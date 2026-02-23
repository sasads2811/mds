import uuid

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
