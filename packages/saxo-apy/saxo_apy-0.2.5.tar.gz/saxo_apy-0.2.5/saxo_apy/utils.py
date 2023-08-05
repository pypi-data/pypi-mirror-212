"""Utils used by SaxoOpenAPIClient."""

import json
from datetime import datetime, timezone
from http import HTTPStatus
from pprint import pformat
from typing import Dict, Optional
from urllib.parse import urlencode

from httpx import Response
from loguru import logger
from pydantic import AnyHttpUrl, parse_obj_as

from .models import APIResponseError, HttpsUrl, OpenAPIAppConfig, StreamingMessage
from .version import VERSION

KNOWN_ERRORS = {
    HTTPStatus.BAD_REQUEST: "invalid request sent",
    HTTPStatus.UNAUTHORIZED: "access token missing, incorrect, or expired",
    HTTPStatus.FORBIDDEN: (
        "you are not authorized to access this resource - check if you are logged in with write permissions and/or "
        "market data has been enabled"
    ),
    HTTPStatus.NOT_FOUND: (
        "requested resource or entity the request operates on could not be found "
        "(or you don't have the required permissions for the requested entity)"
    ),
    HTTPStatus.METHOD_NOT_ALLOWED: "the requested method is not valid for this endpoint",
    HTTPStatus.INTERNAL_SERVER_ERROR: (
        "server error occurred, please ensure your request is valid and notify Saxo support if this error persists"
    ),
}


def configure_logger(log_sink: str, log_level: str) -> None:
    """Set defaults for log config."""
    logger.add(
        log_sink,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS!UTC}Z {thread:12} {level:8} {module:16} {line:5} {function:25} {message}"
        ),
        level=log_level,
        enqueue=True,
    )


def make_default_session_headers() -> Dict:
    """Set default HTTP session."""
    headers: Dict[str, str] = {
        "accept": "application/json; charset=utf-8",
        "accept-encoding": "gzip",
        "user-agent": f"saxo-apy/{VERSION}",
        "connection": "keep-alive",
        "cache-control": "no-cache",
    }
    return headers


def unix_seconds_to_datetime(timestamp: int) -> datetime:
    """Convert unix seconds to human-readable timestamp."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def validate_redirect_url(app_config: OpenAPIAppConfig, redirect_url: Optional[AnyHttpUrl]) -> AnyHttpUrl:
    """Check if provided redirect URL for login is valid - or default to config."""
    if not redirect_url:
        # defaults to first available localhost redirect for convenience
        _redirect_url: AnyHttpUrl = [url for url in app_config.redirect_urls if url.host == "localhost"][0]
    else:
        assert (
            redirect_url in app_config.redirect_urls
        ), f"redirect url {redirect_url} not available in app config - see client.available_redirect_urls"
        _redirect_url = redirect_url
    return _redirect_url


def construct_auth_url(app_config: OpenAPIAppConfig, redirect_url: AnyHttpUrl, state: str) -> HttpsUrl:
    """Parse app_config to generate auth URL."""
    auth_request_query_params = {
        "response_type": "code",
        "client_id": app_config.client_id,
        "state": state,
        "redirect_uri": redirect_url,
    }

    return parse_obj_as(
        HttpsUrl,
        app_config.auth_endpoint + "?" + urlencode(auth_request_query_params),
    )


def handle_api_response(response: Response) -> Response:
    """Handle response from OpenAPI."""
    # parse response details
    status_code = HTTPStatus(response.status_code)
    status_phrase = status_code.name.replace("_", " ")
    elapsed = response.elapsed

    # headers set when request is sent
    request_id = response.request.headers.get("x-request-id")
    env = response.request.headers.get("x-openapi-env")
    client_ts = response.request.headers.get("x-client-timestamp")

    # header returned by OpenAPI
    x_correlation = response.headers.get("x-correlation")
    has_json_content = (
        response.headers.get("content-type") and "application/json" in response.headers.get("content-type").lower()
    )

    # determine if response is known error to customize error message
    error_msg = None
    known_error = KNOWN_ERRORS.get(status_code)
    if known_error:
        error_msg = known_error
    elif not response.is_success:
        error_msg = "unknown error occurred - investigate response details for more information"

    if error_msg:  # something has gone wrong
        if has_json_content:
            error_msg += f" - response content:\n{pformat(response.json(), width=120, indent=2)}"

        exc = APIResponseError(
            f"status: {status_code} - {status_phrase}\n"
            f"error: {error_msg}\n"
            f"client request id: {request_id}\n"
            f"server trace id: {x_correlation}\n"
            f"timestamp (UTC): {client_ts} - elapsed: {elapsed} - env: {env}"
        )
        logger.error(f"error response received from API:\n{exc}")
        raise exc

    logger.success(
        f"success response received with status: {status_code} - {status_phrase}, time taken: {elapsed}, "
        f"client request id: {request_id}, server trace id: {x_correlation}"
    )
    return response


def decode_streaming_message(message: bytes) -> StreamingMessage:
    """Decode streaming message byte and convert to dict."""
    message_id = int.from_bytes(message[0:8], byteorder="little")
    ref_id_len = int(message[10])
    ref_id = message[11 : 11 + ref_id_len].decode()
    format = int(message[11 + ref_id_len])
    if format != 0:
        raise RuntimeError(f"unsupported payload format received on streaming connection: {format}")
    payload_size = int.from_bytes(message[12 + ref_id_len : 16 + ref_id_len], byteorder="little")
    payload = message[16 + ref_id_len : 16 + ref_id_len + payload_size].decode()
    deserialized = json.loads(payload)
    return StreamingMessage(msg_id=message_id, ref_id=ref_id, data=deserialized)
