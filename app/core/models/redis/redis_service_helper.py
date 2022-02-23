import json

from .helper import exist, set_json, get_json_with_root_key, read_db, delete_db, set_json_with_path, expiry_db


async def check_if_visitor_key_exists(conn, key):
    return await exist(conn, key)


async def add_redis_key_with_path(conn, key, value, path='.'):
    return await set_json_with_path(conn, key, value, path)


async def get_conversation_from_redis(conn, key):
    result = await get_json_with_root_key(conn, key)
    return json.loads(result) if result else {}


async def set_session_expiry(conn, session_id, expiry_time):
    await expiry_db(conn, session_id, expiry_time)


async def remove_session_from_visitor(conn, visitor_key):
    await set_json(conn, visitor_key, "[]")


async def get_unifonic_public_id(conn, session_id, path):
    return await get_json_with_root_key(conn, session_id, path)


async def remove_redis_bot_channel_configuration(conn, key):
    await delete_db(conn, key)
