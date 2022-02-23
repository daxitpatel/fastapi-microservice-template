from ...models import sql_scripts

__all__ = ['add_test_visitor', 'get_test_visitor_id']


async def add_test_visitor(conn, message):
    async with conn.cursor() as cursor:
        sql_stmt = sql_scripts['add_test_visitor']
        params = {
            'unique_user_key': message.visitor_key,
            'created_at': message.utc_timestamp,
        }
        await cursor.execute(sql_stmt, params)
        message.visitor_id = cursor.lastrowid
        message.is_new_visitor = False
        if cursor.rowcount == 1:
            message.is_new_visitor = True


async def get_test_visitor_id(conn, message):
    async with conn.cursor() as cursor:
        sql_stmt = sql_scripts['get_test_visitor_id']
        params = {
            'unique_user_key': message.visitor_key
        }
        await cursor.execute(sql_stmt, params)
        row = await cursor.fetchone()
        message.visitor_id = row['id'] if row else None
