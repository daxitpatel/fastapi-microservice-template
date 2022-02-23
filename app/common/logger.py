import logging
import os
from logging.handlers import TimedRotatingFileHandler

from pygelf import GelfUdpHandler
from starlette_context import context

from app.common.constants import YYYY_MM_DD_HH_MM_SS
from app.common.utils import make_dir

__all__ = ['configure_logging']

LOCAL_LOGGER_LOG_FORMAT = '[%(asctime)s] [%(levelname)s] [%(correlation_id)s] ' \
                          '[%(method)s] [%(path_info)s] [%(query_string)s] ' \
                          '[%(pathname)s] %(funcName)s: %(lineno)d : %(message)s] ' \
                          '[%(ip_address)s] [%(http_origin)s] [%(user_agent)s] '

CONSOLE_LOG_FORMAT = "[%(asctime)s,%(msecs)s] %(levelname)s in %(funcName)s: %(message)s"


def configure_logging(app):
    """ Logger configuration with App. """

    # Attach logger with Application
    logging.basicConfig(format=CONSOLE_LOG_FORMAT, datefmt=YYYY_MM_DD_HH_MM_SS)
    app.logger = logging.getLogger(__name__)
    app.logger.setLevel(logging.INFO)

    if app.config.ENABLE_GRAYLOG:
        configure_graylog(app)
    else:
        configure_file_logging(app)


def configure_file_logging(app):
    """ Configure logger with local log file """

    log_folder_location = os.path.abspath(os.path.join(__file__, '..', '..', 'data', 'logs'))

    make_dir(log_folder_location)

    app.logger.setLevel(logging.INFO)
    log_file = '{0}/log'.format(log_folder_location)
    handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, encoding='utf8', backupCount=1825)
    handler.setLevel(logging.INFO)

    formatter = FileLoggerFormatter(LOCAL_LOGGER_LOG_FORMAT)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


def configure_graylog(app):
    """ Log configuration with Graylog """

    additional_fields = {
        "app": app.config.SERVICE_NAME,
        "facility": app.config.PRODUCT,
        "environment": app.config.ENVIRONMENT
    }

    gelf_upd_handler = GelfUdpHandler(host=app.config.GL_SERVER,
                                      port=app.config.GL_PORT,
                                      include_extra_fields=True,
                                      compress=False,
                                      chunk_size=1300,
                                      **additional_fields)

    if app.config.DEBUG:
        gelf_upd_handler.debug = True
        app.logger.setLevel(logging.DEBUG)

    app.logger.addFilter(GrayLogFilter())
    app.logger.addHandler(gelf_upd_handler)


class FileLoggerFormatter(logging.Formatter):
    def format(self, record):
        record = get_http_request_fields(record)
        return super().format(record)


class GrayLogFilter(logging.Filter):

    def filter(self, record):
        get_http_request_fields(record)
        return True


def get_http_request_fields(record):
    """ Integrate Http Request fields with logger """

    record.correlation_id = record.user_id = record.path_info = record.query_string = record.method = \
        record.http_origin = record.ip_address = record.user_agent = record.file_path = ""

    if context.exists():
        record.correlation_id = context.get('correlation_id')
        record.user_id = context.get('user_id')
        record.path_info = context.get('path_info')
        record.query_string = context.get('query_string')
        record.method = context.get('method')
        record.http_origin = context.get('http_origin')
        record.ip_address = context.get('ip_address')
        record.user_agent = context.get('user_agent')
        record.file_path = record.pathname

    return record
