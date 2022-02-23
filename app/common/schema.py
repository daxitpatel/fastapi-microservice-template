from typing import List, Optional

from pydantic import BaseModel, Field


class UnifonicBaseModa(BaseModel):
    class Config:
        extra = "allow"


class ApplicationConfigurationSchema(UnifonicBaseModa):
    application_id: str = Field(..., min_length=1)
    public_id: str = Field(..., min_length=1, max_length=100)
    secret: str = Field(..., min_length=1, max_length=100)
    bot_phone_number: str = None
    configurations: dict = None
    application_slug: str = None
    unifonic_channel_name: str = ""


class BulkChannelConfiguration(UnifonicBaseModa):
    webhook_key: str
    applications: List[ApplicationConfigurationSchema]


class DefaultAPIResponseSchema(UnifonicBaseModa):
    ok: bool | None = True


class UnifonicIncomingMessageSchema(UnifonicBaseModa):
    webhook_key: str = None
    sender: dict
    content: dict
    request_payload: dict
    request_url: str
    is_delay_flow_triggered: bool = False
    is_success_webhook_callback: bool = False
    is_webhook_flow_triggered: bool = False
    extra_parameters: dict | None = {}
    headers: dict | None = {}
    request_headers: dict | None = {}

    class Config:
        extra = "allow"
