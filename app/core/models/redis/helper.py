__all__ = ['save_db', 'read_db', 'delete_db', 'set_json', 'exist',
           'set_json_with_path', 'expiry_db']


async def save_db(db, key, value):
    await db.set(key, value)


async def read_db(db, key):
    return await db.get(key)


async def delete_db(db, key):
    await db.execute_command('DEL', key)


async def expiry_db(db, key, time):
    await db.execute_command('EXPIRE', key, time)


async def set_json(db, key, value):
    await db.execute_command('JSON.SET', key, '.', value)


async def set_json_with_path(db, key, value, path='.'):
    return await db.execute_command('JSON.SET', key, path, value)


async def get_json_with_root_key(db, key, root_key="."):
    result = await db.execute_command('JSON.GET', key, 'NOESCAPE', root_key)
    return result


async def get_rejson_supported_path(path_element):
    if path_element and path_element[0].isdigit():
        return '["{}"]'.format(path_element)
    return path_element


async def exist(redis, key):
    if await redis.execute_command('EXISTS', key):
        return True
    return False
