import aiomysql

from app import app

__all__ = ["mysql_connection_pool_factory", "MySQLConnectionManager"]


async def mysql_connection_pool_factory():
    """ This method is used to create MySQL pool creation """

    return await aiomysql.create_pool(
        minsize=app.config.MYSQL_CONNECTION_POOL_MINIMUM_SIZE,
        maxsize=app.config.MYSQL_CONNECTION_POOL_MAXIMUM_SIZE,
        host=app.config.MYSQL_DATABASE_HOST,
        user=app.config.MYSQL_DATABASE_USER,
        password=app.config.MYSQL_DATABASE_PASSWORD,
        db=app.config.MYSQL_CORE_DATABASE,
        pool_recycle=app.config.MYSQL_CONNECTION_MAX_POOL_RECYCLE_TIME,
        cursorclass=aiomysql.DictCursor
    )


async def get_connection():
    """ This method is used to create MySQL pool creation """

    return await aiomysql.connect(
        host=app.config.MYSQL_DATABASE_HOST,
        user=app.config.MYSQL_DATABASE_USER,
        password=app.config.MYSQL_DATABASE_PASSWORD,
        db=app.config.MYSQL_CORE_DATABASE,
        cursorclass=aiomysql.DictCursor
    )


class MySQLConnectionManager(object):
    def __init__(self):
        self.conn = None

    async def __aenter__(self):
        # Todo: Due to this open issue in connection pool in aiomysql(https://github.com/aio-libs/aiomysql/issues/519)
        #  removing use of connection pooling

        self.conn = await get_connection()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
