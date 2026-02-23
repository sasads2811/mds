import uuid
from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.base import Base

class RackModel(Base):
    __tablename__ = "rack_model"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    serial_number: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    total_units: Mapped[int] = mapped_column(Integer, nullable=False)
    max_power_watts: Mapped[int] = mapped_column(Integer, nullable=False)

    placements = relationship(
        "RackDeviceModel",
        back_populates="rack",
        cascade="all, delete-orphan",
    )