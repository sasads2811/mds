import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.infrastructure.db.models.device_model import DeviceModel
from app.domain.device.entity import Device


class DeviceRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_device_by_id(self, device_id: uuid.UUID) -> Device:
        q = select(DeviceModel).where(DeviceModel.id == device_id)

        result = self.session.execute(q)

        result = result.scalars().first()

        return result

    def get_all(self):
        q = select(DeviceModel)

        result = self.session.execute(q)

        return result.scalars().all()

    def create(self, device: Device) -> Device:
        model = DeviceModel(
            name=device.name,
            description=device.description,
            serial_number=device.serial_number,
            rack_units=device.rack_units,
            power_watts=device.power_watts,
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        device.id = model.id
        return device

    def save(self, device: Device) -> Device:
        result = self.session.get(DeviceModel, device.id)

        result.name = device.name
        result.description = device.description
        result.serial_number = device.serial_number
        result.rack_units = device.rack_units
        result.power_watts = device.power_watts

        self.session.commit()
        self.session.refresh(result)

        return device
