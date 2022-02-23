from fastapi import FastAPI, APIRouter
from inspect import getmembers, isclass
from starlette.middleware import Middleware

import app.common.exception as exceptions
from app.common.logger import configure_logging
from app.common.utils import exception_handler, custom_exception_handler
from app.config import Configurations
from app.middlewares import RequestLoggerMiddleware, RequestCatcherMiddleware


def create_app():
    """ Create application with FastAPI """

    middleware = [Middleware(RequestCatcherMiddleware), Middleware(RequestLoggerMiddleware)]
    app = FastAPI(title=__name__, middleware=middleware)
    router = APIRouter(prefix='/api')
    app.config = Configurations()
    configure_logging(app)
    map_exception_handlers(app)

    return app, router


def map_exception_handlers(app):
    """ Map all custom exceptions with application """

    # Custom exception binding

    business_exception = dict(getmembers(exceptions, isclass))
    [app.add_exception_handler(exception_class, custom_exception_handler)
     for exception, exception_class in business_exception.items() if exception in exceptions.__all__]

    # Handle Internal Server Error
    app.add_exception_handler(Exception, exception_handler)
