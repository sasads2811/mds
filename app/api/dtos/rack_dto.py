import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RackCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str
    serial_number: str
    total_units: int
    max_power_watts: int


class RackResponse(RackCreate):
    id: uuid.UUID


class EditRack(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None
    total_units: Optional[int] = None
    max_power_watts: Optional[int] = None
