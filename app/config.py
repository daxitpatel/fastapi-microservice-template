import os
import json
from distutils.util import strtobool

from pydantic import BaseSettings

__all__ = ["Configurations"]

_REDIS_URL = "redis://:{pwd}@{host}:{port}/{db_index}"


class Configurations(BaseSettings):
    """Environment Variable configuration"""

    def __init__(self):
        super().__init__()
        self.app_config()
        self.logging_config()
        self.mysql_config()
        self.es_config()
        self.redis_config()
        self.rabbitmq_config()
        self.utility_config()

    @classmethod
    def app_config(cls):
        """Basic Application level configurations"""

        cls.SERVICE_NAME = os.environ.get("FASTAPI_SERVICE_NAME", "fastapi-microservice")
        cls.PRODUCT = os.environ.get("PRODUCT")  # no default ?
        cls.ENVIRONMENT = os.environ.get("ENVIRONMENT")
        cls.DEBUG = strtobool(os.environ.get("DEBUG", "0"))
        cls.PORT = int(os.environ.get("FASTAPI1_SERVICE_PORT", 5000))
        cls.LOG_LEVEL = "INFO" if not cls.DEBUG else "DEBUG"

    @classmethod
    def logging_config(cls):
        """ " Logger configurations"""

        cls.GL_SERVER = os.environ.get("GL_SERVER", "localhost")
        cls.GL_PORT = int(os.environ.get("GL_PORT", 12201))
        cls.ENABLE_GRAYLOG = int(os.environ.get("ENABLE_GRAYLOG", 0))

    @classmethod
    def mysql_config(cls):
        """MySQL configurations"""

        cls.MYSQL_DATABASE_HOST = os.environ.get("MYSQL_DATABASE_HOST")
        cls.MYSQL_CORE_DATABASE = os.environ.get("MYSQL_DATABASE", "fastapi_service_db")
        cls.MYSQL_DATABASE_USER = os.environ.get("MYSQL_DATABASE_USER")
        cls.MYSQL_DATABASE_PASSWORD = os.environ.get("MYSQL_DATABASE_PASSWORD")

        cls.MYSQL_CONNECTION_POOL_MINIMUM_SIZE = int(
            os.environ.get("MYSQL_CONNECTION_POOL_MINIMUM_SIZE", 5)
        )
        cls.MYSQL_CONNECTION_POOL_MAXIMUM_SIZE = int(
            os.environ.get("MYSQL_CONNECTION_POOL_MAXIMUM_SIZE", 10)
        )
        cls.MYSQL_CONNECTION_MAX_POOL_RECYCLE_TIME = int(
            os.environ.get("MYSQL_CONNECTION_MAX_POOL_RECYCLE_TIME", 10)
        )

    @classmethod
    def es_config(cls):
        """Elasticsearch configurations"""

        cls.ELASTICSEARCH_SERVICE_URL = os.environ.get("ELASTICSEARCH_SERVICE_URL")
        cls.ES_ACCESS_TOKEN = os.environ.get("ES_ACCESS_TOKEN")

    @classmethod
    def redis_config(cls):
        """Redis Configuration"""

        cls.REDIS_HOST = os.environ.get("REDIS_HOST")
        cls.REDIS_PORT = os.environ.get("REDIS_PORT")
        cls.REDIS_DATABASE = os.environ.get("REDIS_DATABASE", "0")
        cls.REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
        cls.REDIS_URL = _REDIS_URL.format(
            pwd=os.environ.get("REDIS_PASSWORD"),
            host=os.environ.get("REDIS_HOST"),
            port=os.environ.get("REDIS_PORT"),
            db_index=os.environ.get("REDIS_DATABASE"),
        )

    @classmethod
    def rabbitmq_config(cls):
        """RabbitMQ Configurations"""
        cls.RABBIT_MQ_HOST = os.environ.get("RABBIT_MQ_HOST")
        cls.RABBIT_MQ_HOST_URL = os.environ.get("RABBIT_MQ_HOST_URL")
        cls.RABBIT_MQ_PORT = int(os.environ.get("RABBIT_MQ_PORT"))
        cls.RABBIT_MQ_V_HOST = os.environ.get("RABBIT_MQ_V_HOST", "%2f")
        cls.RABBIT_MQ_USERNAME = os.environ.get("RABBIT_MQ_USERNAME")
        cls.RABBIT_MQ_PASSWORD = os.environ.get("RABBIT_MQ_PASSWORD")
        cls.RABBIT_MQ_HEARTBEAT = os.environ.get("RABBIT_MQ_HEARTBEAT")

        cls.RABBITMQ_CONNECTION_POOL_MAX_SIZE = int(
            os.environ.get("RABBITMQ_CONNECTION_POOL_MAX_SIZE", "100")
        )
        cls.RABBITMQ_CHANNEL_POOL_MAX_SIZE = int(
            os.environ.get("RABBITMQ_CHANNEL_POOL_MAX_SIZE", "1024")
        )
        cls.RABBIT_MQ_PREFETCH_COUNT = int(
            os.environ.get("RABBIT_MQ_PREFETCH_COUNT", 1)
        )

    @classmethod
    def utility_config(cls):
        """Utility configurations"""

        cls.CHANNEL_SERVICE_HOST_NAME = os.environ.get(
            "CHANNEL_SERVICE_HOST_NAME", "some-other-microservice"
        )

        cls.SCHEDULER_SECRET = os.environ.get("SCHEDULER_SECRET")
