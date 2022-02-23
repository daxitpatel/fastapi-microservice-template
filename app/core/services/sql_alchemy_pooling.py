
class SessionHandler(object):
    """
    This class is use to handle the DB connection. This class can be use with ``with`` statement.
    - At the starting of the ``with`` statement it will invoke ``__enter__`` method to create the connection
    - At the end of the ``with`` statement it will invoke ``__exit__`` method to close the connection

    Steps to use:
        Step 1: Configure ORM
        Step 2: from DataAccessLib.database.connect import SessionHandler
        Step 3: Use ``SessionHandler`` with ``with`` statement to create the connection

    Example:
        from DataAccessLib.database.config import configure_orm

        engine, Session = configure_orm(SQL_DATABASE_USER="Your SQL database user",
                         SQL_DATABASE_PASSWORD="Your SQL database password",
                         SQL_DATABASE_HOST="Your SQL database host",
                         SQL_DATABASE_DB="Your SQL database DB",
                         SQL_DATABASE_CONNECTION_POOL_SIZE="SQL database pool connection size",
                         SQL_DATABASE_CONNECTION_POOL_MAX_OVERFLOW_SIZE="SQL database max connection pool size")

    """

    def __init__(self, session_maker):
        self.session = None
        self.session_maker = session_maker

    def __enter__(self):
        """It's invoking ``connect`` method to create the connection"""
        self.session = connect(self.session_maker)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """It invoking ``close`` method to close the connection"""
        close(self.session)


def connect(session_maker):
    """Create DB connection object"""
    return session_maker()


def close(session):
    if session is not None:
        """Close DB connection"""
        session.close()
