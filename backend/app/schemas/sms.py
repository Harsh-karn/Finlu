from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class SMSIngestRequest(BaseModel):
    raw_sms: str
    received_at: datetime
    device_api_key: str

class SMSDeviceRegisterRequest(BaseModel):
    device_name: str

class SMSDeviceResponse(BaseModel):
    id: UUID
    device_name: str
    api_key: str # Only returned once upon registration
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class SMSDeviceListResponse(BaseModel):
    id: UUID
    device_name: str
    is_active: bool
    last_sync: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
