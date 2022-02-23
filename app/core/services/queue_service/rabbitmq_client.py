import asyncio
import aio_pika

from app.common import QueueEnum
from app.core.services.queue_service.consumer import ConsumerTestMessageListener
from app.core.services.queue_service.common import get_queue_consumers_count

__all__ = ['get_connection', 'get_channel', 'rmq_pool_factory', 'load_consumers', 'queue_init',
           'restart_dead_consumers']

consumer_map = {
    QueueEnum.TEST_MESSAGE.name: ConsumerTestMessageListener
}


async def get_connection(app):
    """ This method is used to create RabbitMQ connection """
    url = f'amqp://{app.config.RABBIT_MQ_USERNAME}:{app.config.RABBIT_MQ_PASSWORD}@' \
          f'{app.config.RABBIT_MQ_HOST}:{app.config.RABBIT_MQ_PORT}/' \
          f'{app.config.RABBIT_MQ_V_HOST}?heartbeat={app.config.RABBIT_MQ_HEARTBEAT}' \
          '&retry_delay=3&connection_attempts=3&blocked_connection_timeout=300'

    return await aio_pika.connect_robust(url=url)


async def get_channel(app) -> aio_pika.Channel:
    """ This method is used to create a channel """

    async with app.rmq_connection_pool.acquire() as connection:
        return await connection.channel()


async def restart_dead_consumers():
    loop = asyncio.get_running_loop()
    for data in QueueEnum:
        if data.value['worker']:
            active_consumer = await get_queue_consumers_count(data.value['queue_name'])
            dead_workers = data.value['worker'] - active_consumer
            if dead_workers > 0:
                await load_consumers(loop, data.name, data.value['queue_name'], dead_workers)


async def rmq_pool_factory(app):
    """ This method is used to create a pool of channel """

    app.rmq_connection_pool = aio_pika.pool.Pool(get_connection,
                                                 app,
                                                 max_size=app.config.RABBITMQ_CONNECTION_POOL_MAX_SIZE)

    channel_pool = aio_pika.pool.Pool(get_channel,
                                      app,
                                      max_size=app.config.RABBITMQ_CHANNEL_POOL_MAX_SIZE)
    return channel_pool


async def load_consumers(loop, consumer, queue_name, consumer_count):
    """ This method is used to add consumers for the requested queue with requested consumer count

    :param loop :-  Async Event loop
    :param consumer:- Consumer name
    :param queue_name:- RabbitMQ queue name
    :param  consumer_count:- Consumer count
    """

    for _ in range(consumer_count):
        service = consumer_map[consumer](queue_name=queue_name)
        loop.create_task(service.run())


async def queue_init(app):
    """ This method is used to start RabbitMQ operations with application start

    Operations:
        - Declare exchange & queue
        - Map declared queue & exchange
        - Start consumer
    """

    loop = asyncio.get_running_loop()
    for data in QueueEnum:
        async with app.rmq_channel_pool.acquire() as channel:
            # Declare exchange
            exchange = await channel.declare_exchange(
                name=data.value["exchange_name"],
                type=data.value["exchange_type"],
                durable=True,
            )
            # Queue declare
            queue = await channel.declare_queue(
                name=data.value["queue_name"],
                durable=True
            )
            # Queue <> Exchange binding
            await queue.bind(
                exchange=exchange, routing_key=data.value["route_key"]
            )

        # Load Consumers
        if data.name in consumer_map:
            await load_consumers(loop, data.name, data.value['queue_name'], data.value['worker'])
