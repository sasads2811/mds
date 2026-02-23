import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str | None = None
    serial_number: str
    rack_units: int
    power_watts: int


class DeviceResponse(DeviceCreate):
    id: uuid.UUID


class EditDevice(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None
    rack_units: Optional[int] = None
    power_watts: Optional[int] = None
