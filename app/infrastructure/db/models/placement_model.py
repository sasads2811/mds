import uuid
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base


class RackDeviceModel(Base):
    __tablename__ = "rack_devices"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    rack_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rack_model.id", ondelete="CASCADE"),
        nullable=False,
    )

    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("device_model.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    start_unit: Mapped[int] = mapped_column(Integer, nullable=False)
    end_unit: Mapped[int] = mapped_column(Integer, nullable=False)

    rack = relationship("RackModel", back_populates="placements")
    device = relationship("DeviceModel", back_populates="placement")
