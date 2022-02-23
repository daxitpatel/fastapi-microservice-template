import redis.asyncio as redis


async def redis_store(app):
    return await redis.from_url(app.config.REDIS_URL, decode_responses=True)
