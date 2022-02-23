import os
from enum import Enum

__all__ = ['RedisKeyEnum', 'HttpStatusCodeEnum', 'HttpMethodEnum', 'QueueEnum', 'DefaultStatus']


class RedisKeyEnum(Enum):
    test_account_settings = "test_account_{account_id}"


class HttpStatusCodeEnum(Enum):
    SUCCESS = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    CONFLICT = 409
    RATE_LIMIT = 429
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


class HttpMethodEnum(Enum):
    POST = 'POST'
    PUT = 'PUT'
    GET = 'GET'
    DELETE = 'DELETE'


class QueueEnum(Enum):
    TEST_MESSAGE = {
        'route_key': 'test-incoming-message-handler',
        'queue_name': 'test-incoming-message-handler-queue-dx',
        'exchange_type': 'direct',
        'exchange_name': 'wotnot.direct',
        'worker': int(os.environ.get("TEST_INCOMING_MESSAGE_HANDLER_QUEUE_WORKER", 10)),  # TODO to move to config
        "prefetch_count": int(os.environ.get("TEST_INCOMING_MESSAGE_PREFETCH_COUNT", 20))  # TODO to move to config
    }
    TEST_MESSAGE_FAILED = {
        'route_key': 'test-incoming-message-handler-failed',
        'queue_name': 'test-incoming-message-handler-queue-failed-dx',
        'exchange_type': 'direct',
        'exchange_name': 'wotnot.direct',
        'worker': 0}


class DefaultStatus(Enum):
    STATUS = 1
