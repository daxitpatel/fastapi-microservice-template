from app.manage import create_app

# Create App
app, router = create_app()


@app.on_event("startup")
async def init_app():
    """ Initialise app configuration on app startup """
    # To avoid circular import error in RabbitMQ clients
    from app.core.models.redis import redis_store
    from app.core.services.queue_service.rabbitmq_client import rmq_pool_factory, queue_init

    app.redis_store = await redis_store(app)
    app.rmq_channel_pool = await rmq_pool_factory(app)
    await queue_init(app)


@app.on_event("shutdown")
async def terminate_app():
    """ Terminate app configuration on app shutdown """

    await app.redis_store.close()
    await app.rmq_connection_pool.close()


# import APIs endpoints
from .apis import *

# Include router
app.include_router(router)
