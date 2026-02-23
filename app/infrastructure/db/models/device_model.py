import uuid
from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.base import Base

class DeviceModel(Base):
    __tablename__ = "device_model"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    serial_number: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    rack_units: Mapped[int] = mapped_column(Integer, nullable=False)
    power_watts: Mapped[int] = mapped_column(Integer, nullable=False)

    placement = relationship(
        "RackDeviceModel",
        back_populates="device",
        uselist=False,
        cascade="all, delete-orphan",
    )