
__all_ = ['publish_message']

import json
from typing import Any

import aio_pika

from app import app


async def publish_message(exchange_name: str, exchange_type: str, route_key: str, payload: Any,
                          headers: dict = {}, durable=True):
    async with app.rmq_channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange(name=exchange_name, type=exchange_type, durable=durable)
        message = aio_pika.Message(
            body=json.dumps(payload).encode(),
            headers=headers,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT.value,
        )
        await exchange.publish(message=message, routing_key=route_key)