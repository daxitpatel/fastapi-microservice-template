import asyncio
import json
import uuid
from base64 import b64encode
from uuid import uuid4

from aio_pika import AMQPException
from starlette_context import _request_scope_context_storage

from app import app
from ....common import (RABBITMQ_QUEUES_REPORT_API, invoke_http_request, HttpMethodEnum, WT_CORRELATION_ID,
                        RABBITMQ_QUEUES_DETAILS_API)

__all__ = ['get_queues_consumer_count', 'get_queues_consumer_count', 'channel_basic_consume',
           'handle_consumer_callback', 'publish_failed_message', 'get_queue_consumers_count']

CONSUMER_TAG = str(uuid4())

async def get_queues_consumer_count():
    """RabbitMQ API to get queues details and it's active consumers"""
    from app import app

    secret = '{}:{}'.format(app.config.RABBIT_MQ_USERNAME, app.config.RABBIT_MQ_PASSWORD)
    endpoint = RABBITMQ_QUEUES_REPORT_API.format(rabbitmq_host=app.config.RABBIT_MQ_HOST_URL)
    token = b64encode(bytes(secret, 'utf-8')).decode("ascii")
    header = {'Authorization': 'Basic {}'.format(token)}
    response, status_code = await invoke_http_request(endpoint, HttpMethodEnum.GET.value, header)
    return {queue['name']: queue['consumers'] for queue in response}


async def get_queue_consumers_count(queue_name):
    """ This function is used to get the consumer count for the running service POD """
    from app import app

    secret = '{}:{}'.format(app.config.RABBIT_MQ_USERNAME, app.config.RABBIT_MQ_PASSWORD)
    endpoint = RABBITMQ_QUEUES_DETAILS_API.format(rabbitmq_host=app.config.RABBIT_MQ_HOST_URL,
                                                  virtual_host=app.config.RABBIT_MQ_V_HOST,
                                                  queue=queue_name)
    token = b64encode(bytes(secret, 'utf-8')).decode("ascii")
    header = {'Authorization': 'Basic {}'.format(token)}
    response, status_code = await invoke_http_request(endpoint, HttpMethodEnum.GET.value, header)
    count = 0
    for consumer in response['consumer_details']:
        if consumer['consumer_tag'] == CONSUMER_TAG:
            count += 1
    return count


async def channel_basic_consume(callback, queue_name, prefetch_count=1, auto_ack=False):
    """ This method is used to consume the received message """

    async with app.rmq_connection_pool.acquire() as connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=prefetch_count)
        queue = await channel.declare_queue(queue_name, durable=True)
        await asyncio.sleep(5)
        await queue.consume(callback, no_ack=auto_ack,  consumer_tag=CONSUMER_TAG)


async def handle_consumer_callback(consumer, message, handle_success, handle_failed, handle_redelivered):
    """ This method is used to process consumed message

    Steps:
        - Log consumed message
        - Call callback for processing message
        - Handle exception if any
        - Acknowledge message
    """
    correlation_id = message.headers[WT_CORRELATION_ID] = message.headers.get(WT_CORRELATION_ID, str(uuid.uuid4()))
    _request_scope_context_storage.set({"correlation_id": correlation_id})

    name = consumer.__class__.__name__
    app.logger.info(f"AMQP {name}")

    payload = json.loads(message.body.decode('utf-8'))
    payload.update({"headers": message.headers})
    try:
        await handle_success(payload) if not message.redelivered else await handle_redelivered(payload)

    except AMQPException as e:
        app.logger.exception(f'AMQP: {consumer} -> Error while processing '
                             f'{message.body.decode("utf-8")} -> error {e}')
        await consumer.run()

    except Exception as e:
        app.logger.exception(f'AMQP: {consumer} -> Error while processing '
                             f'{message.body.decode("utf-8")} -> error {e}')
        await handle_failed(payload)

    finally:
        await message.channel.basic_ack(delivery_tag=message.delivery_tag)


async def publish_failed_message(params, queue_enum):
    from .publisher import publish_message
    await publish_message(exchange_name=queue_enum.get('exchange_name'),
                          route_key=queue_enum.get('route_key'),
                          payload=params,
                          exchange_type=queue_enum.get('exchange_type'))
