from fastapi.responses import Response

from app import app
from app.common import (
    APP_READINESS_API, APP_LIVENESS_API, APP_TERMINATION_API, RABBITMQ_CONSUMER_HEALTH_TEST_API,
    HttpStatusCodeEnum
)
from app.core.services.queue_service.rabbitmq_client import restart_dead_consumers

__all__ = ['queue_service_health', 'service_status']


@app.get(RABBITMQ_CONSUMER_HEALTH_TEST_API)
async def queue_service_health():
    """ This method is resolved the rabbitmq consumer auto discard issue """
    await restart_dead_consumers()
    return Response(status_code=HttpStatusCodeEnum.NO_CONTENT.value)


@app.get(APP_READINESS_API)
@app.get(APP_LIVENESS_API)
@app.get(APP_TERMINATION_API)
async def service_status():
    return Response(status_code=HttpStatusCodeEnum.NO_CONTENT.value)
