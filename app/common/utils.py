import os
import random
import string
from configparser import ConfigParser
from datetime import datetime
from io import StringIO
from typing import Union
from uuid import uuid4

import pytz
import shortuuid
from aiohttp.client_exceptions import ContentTypeError
from aiohttp.web import HTTPException
from aiohttp_retry import ExponentialRetry
from aiohttp_retry.client import RetryClient
from fastapi.responses import JSONResponse
from starlette_context import context

from app.common import HttpStatusCodeEnum
from app.common.errors import errors
from .constants import DT_FMT_ymdHMSf


def exception_handler(req, exc):
    """ Exception Handler
    :param req - Request object
    :param exc - Exception

    :returns - Generic error response with status code 500
    """

    return JSONResponse(content=errors['Exception'], status_code=500)


def custom_exception_handler(req, exc):
    """ Custom exception handler
    :param req - Request object
    :param exc - Exception

    :returns - Define error message for custom exception
    """

    req.app.logger.info(f"Custom Exception {exc.__class__.__name__} on {req.url.path}")
    return JSONResponse(content=errors.get(exc.__class__.__name__, errors['Exception']),
                        status_code=errors.get(exc.__class__.__name__, errors['Exception'])['status'])


def get_unique_key():
    timestamp = datetime.now().strftime('%H%M%S%f')
    random_str = timestamp + ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(8))
    uuid_str = shortuuid.ShortUUID().random(length=12)
    return '{}{}'.format(uuid_str, random_str)


def make_dir(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def generate_webhook_key():
    return str(uuid4()).replace('-', '')


def get_current_timestamp(timezone=pytz.utc):
    return datetime.now(tz=timezone)


def datetime_to_str(date_time, str_format=DT_FMT_ymdHMSf):
    return date_time.strftime(str_format)


def get_timestamp(timezone=pytz.utc):
    from datetime import datetime
    return datetime.now(tz=timezone)


def convert_datetime_to_iso(date_time):
    return date_time.replace(tzinfo=pytz.utc).isoformat()


def get_utc_timestamp():
    return datetime_to_str(get_current_timestamp())


def get_utc_datetime():
    return datetime.now(tz=pytz.utc)


def read_properties_file(file_path):
    with open(file_path) as f:
        config = StringIO()
        config.write('[dummy_section]\n')
        config.write(f.read().replace('%', '%%'))
        config.seek(0, os.SEEK_SET)
        cp = ConfigParser()
        cp.read_file(config)
        return dict(cp.items('dummy_section'))


def get_request_correlation_id(correlation_id):
    return correlation_id if correlation_id else uuid4().__str__()


def is_success_request(status_code):
    return 200 <= status_code <= 299


def requests_retry_session():
    """ Add retry session for HttpRequest """

    retry_option = ExponentialRetry(
        attempts=3,
        start_timeout=0.5,
        factor=1.5,
        statuses=(HttpStatusCodeEnum.RATE_LIMIT.value, HttpStatusCodeEnum.INTERNAL_SERVER_ERROR.value,
                  HttpStatusCodeEnum.BAD_GATEWAY.value, HttpStatusCodeEnum.SERVICE_UNAVAILABLE.value,
                  HttpStatusCodeEnum.GATEWAY_TIMEOUT.value)
    )
    return retry_option


async def _get_response(response) -> Union[dict, str]:
    """ Get json/text response """

    try:
        return await response.json()
    except ContentTypeError:
        return await response.text()


async def invoke_http_request(endpoint: str, method: str, headers: dict = {}, payload: dict = {}, timeout: int = 60):
    """ HttpRequest Maker
    :param  endpoint - URL
    :param method - Http Method
    :param headers - Request header
    :param payload - Request body
    :param timeout - Request timeout

    :returns - Response & status code from Http request call
    """

    retry_session = requests_retry_session()
    response = status = None
    try:
        async with RetryClient(retry_options=retry_session, headers=headers) as session:
            async with session.request(method=method, url=endpoint, json=payload, ssl=False,
                                       timeout=timeout) as response:
                response, status_code = await _get_response(response), response.status
        return response, status_code
    except HTTPException:
        return response, status
    except TimeoutError:
        return response, status


def get_visitor_key(visitor_key):
    return visitor_key.replace("+", "")
