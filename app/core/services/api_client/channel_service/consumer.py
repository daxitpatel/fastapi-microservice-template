from app import app
from app.common.utils import invoke_http_request
from .constants import (PORT, SEND_TEST_MESSAGE_API)
from ..constants import HTTP_GET, HTTP_POST
from ..helper import get_endpoint, get_headers

__all__ = ['ChannelService']


class ChannelService:
    def __init__(self, request_user_id, correlation_id):
        self.request_user_id = request_user_id
        self.headers = get_headers(correlation_id, request_user_id)

    def send_unifonic_message(self, payload):
        payload = {
            "public_id": payload['public_id'],
            "secret": payload['secret'],
            "recipient": payload['recipient'],
            "content": payload['content']
        }
        return invoke_http_request(self._get_endpoint(SEND_TEST_MESSAGE_API),
                                   HTTP_POST,
                                   self.headers,
                                   payload)

    @staticmethod
    def _get_endpoint(api_path):
        return get_endpoint(host=app.config.CHANNEL_SERVICE_HOST_NAME, port=PORT, endpoint=api_path)
