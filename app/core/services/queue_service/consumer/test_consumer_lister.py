from app.common import UnifonicIncomingMessageSchema
from ..common import (channel_basic_consume, handle_consumer_callback, publish_failed_message)
from .....common import QueueEnum, PREFETCH_COUNT

__all_ = ['ConsumerTestMessageListener']


class ConsumerTestMessageListener:

    def __init__(self, queue_name):
        self.queue_name = queue_name

    @staticmethod
    async def success_callback(payload):
        # Business logic to process the message
        pass

    @staticmethod
    async def failure_callback(params):
        await publish_failed_message(params, QueueEnum.TEST_MESSAGE_FAILED.value)

    async def callback(self, message):
        await handle_consumer_callback(self,
                                       message,
                                       self.success_callback,
                                       self.failure_callback,
                                       handle_redelivered=self.failure_callback)

    async def run(self):
        await channel_basic_consume(self.callback, self.queue_name,
                                    prefetch_count=QueueEnum.TEST_MESSAGE.value[PREFETCH_COUNT])
