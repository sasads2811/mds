from sqlalchemy import select
from sqlalchemy.orm import Session
from app.infrastructure.db.models.device_model import DeviceModel
from app.domain.device.entity import Device


class DeviceRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        q = select(DeviceModel)

        result = self.db.execute(q)

        return result.scalars().all()


    def create(self, device: Device) -> Device:
        model = DeviceModel(
            name=device.name,
            description=device.description,
            serial_number=device.serial_number,
            rack_units=device.rack_units,
            power_watts=device.power_watts,
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        device.id = model.id
        return device