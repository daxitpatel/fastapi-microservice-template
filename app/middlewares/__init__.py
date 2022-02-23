import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette_context.middleware import ContextMiddleware

from app.common.constants import WT_CORRELATION_ID, WT_USER_ID, IGNORE_PATH_LOG

__all__ = ['RequestCatcherMiddleware', 'RequestLoggerMiddleware']


class RequestLoggerMiddleware(BaseHTTPMiddleware):

    @staticmethod
    def ignore_log(request: Request):
        return request.url.path not in IGNORE_PATH_LOG

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """ This method will use to add unique ID for request """

        if self.ignore_log(request):
            request.app.logger.info('Request-Start')
        try:
            response = await call_next(request)

        except Exception as exc:
            request.app.logger.exception(f"Exception on {request.url.path}")
            raise exc

        finally:
            if self.ignore_log(request):
                request.app.logger.info('Request-End')

        return response


class RequestCatcherMiddleware(ContextMiddleware):
    async def set_context(self, request: Request) -> dict:
        """ This method will use to add unique ID for request """

        request_properties = dict(
            correlation_id=request.headers.get(WT_CORRELATION_ID, str(uuid.uuid4())),
            user_id=request.headers.get(WT_USER_ID, '-'),
            path_info=request.url.path,
            query_string=str(request.query_params),
            method=request.method,
            http_origin=request.headers.get('HTTP_ORIGIN', ''),
            ip_address=(request.headers.get('HTTP_X_FORWARDED_FOR', '')
                        or request.headers.get('REMOTE_ADDR', '-')),
            user_agent=request.client.host
        )

        return request_properties
