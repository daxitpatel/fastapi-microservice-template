__all__ = ['fetch_row', 'insert', 'insert_row', 'update_row', 'insert_many', 'delete', 'fetch_rows']


async def fetch_row(conn, sql_stmt, params):
    async with conn.cursor() as cursor:
        await cursor.execute(sql_stmt, params)
        return await cursor.fetchone()


async def fetch_rows(conn, sql_stmt, params):
    async with conn.cursor() as cursor:
        await cursor.execute(sql_stmt, params)
        return await cursor.fetchall()


async def insert(conn, sql_stmt, params):
    async with conn.cursor() as cursor:
        await cursor.execute(sql_stmt, params)
        id = cursor.lastrowid
        row_count = cursor.rowcount
        result = {
            "id": id,
            "row_count": row_count
        }
        return result


async def insert_many(conn, sql_stmt, params):
    async with conn.cursor() as cursor:
        await cursor.executemany(sql_stmt, params)


async def insert_row(conn, sql_stmt, params):
    result = {
        "insert_id": None,
        "rowcount": None
    }
    async with conn.cursor() as cursor:
        await cursor.execute(sql_stmt, params)
        result['insert_id'] = cursor.lastrowid
        result['rowcount'] = cursor.rowcount
    return result


async def update_row(conn, sql_stmt, params):
    async with conn.cursor() as cursor:
        await cursor.execute(sql_stmt, params)
        await conn.commit()


async def delete(conn, sql_stmt, params):
    async with conn.cursor() as cursor:
        await cursor.execute(sql_stmt, params)
        await conn.commit()
