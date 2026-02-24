import uuid
from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.infrastructure.db.models import RackModel, DeviceModel, RackDeviceModel
from app.domain.rack.entity import Rack
from app.domain.device.entity import Device
from app.domain.placement.entity import RackDevice


class RackRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_rack_by_id(self, rack_id: uuid.UUID):
        q = (
            select(
                RackModel.id,
                RackModel.name,
                RackModel.description,
                RackModel.total_units,
                RackModel.max_power_watts,
                RackModel.serial_number,
                func.sum(DeviceModel.power_watts).label("total_power_used"),
            )
            .join(RackDeviceModel, RackModel.placements)
            .join(DeviceModel, RackDeviceModel.device)
            .where(RackModel.id == rack_id)
        ).group_by(
            RackModel.id,
            RackModel.serial_number,
            RackModel.name,
            RackModel.description,
            RackModel.total_units,
            RackModel.max_power_watts,
        )

        result = self.session.execute(q)

        result = result.first()

        return result

    def get_device_by_id(self, device_id: uuid.UUID) -> Device:
        q = select(DeviceModel).where(DeviceModel.id == device_id)

        result = self.session.execute(q)

        result = result.scalars().first()

        return result

    def get_all(self):
        q = select(RackModel)

        result = self.session.execute(q)

        return result.scalars().all()

    def create(self, rack: Rack) -> Rack:
        model = RackModel(
            name=rack.name,
            description=rack.description,
            serial_number=rack.serial_number,
            max_power_watts=rack.max_power_watts,
            total_units=rack.total_units,
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        rack.id = model.id

        return rack

    def save(self, rack: Rack) -> Rack:
        result = self.session.get(RackModel, rack.id)

        result.name = rack.name
        result.description = rack.description
        result.serial_number = rack.serial_number
        result.total_units = rack.total_units
        result.max_power_watts = rack.max_power_watts

        self.session.commit()
        self.session.refresh(result)

        return rack

    def get_rack_devices(self, rack_id: uuid.UUID) -> List[RackDevice]:
        q = select(RackDeviceModel).where(RackDeviceModel.rack_id == rack_id)

        result = self.session.execute(q)

        return result.scalars().all()

    def create_rack_device(
        self, rack_id: uuid.UUID, device_id: uuid.UUID, start_unit: int, end_unit: int
    ) -> RackDevice:
        model = RackDeviceModel(
            rack_id=rack_id,
            device_id=device_id,
            start_unit=start_unit,
            end_unit=end_unit,
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return model

    def get_rack_device_by_rack_and_device_id(
        self, rack_id: uuid.UUID, device_id: uuid.UUID
    ) -> RackDevice:
        q = select(RackDeviceModel).where(
            RackDeviceModel.rack_id == rack_id, RackDeviceModel.device_id == device_id
        )

        result = self.session.execute(q)

        return result.scalars().first()

    def get_devices_by_ids(self, device_ids: list) -> List[Device]:
        q = select(DeviceModel).where(DeviceModel.id.in_(device_ids))

        result = self.session.execute(q)

        models = result.scalars().all()

        devices = [
            Device(
                id=m.id,
                name=m.name,
                description=m.description,
                serial_number=m.serial_number,
                power_watts=m.power_watts,
                rack_units=m.rack_units,
            )
            for m in models
        ]

        return devices

    def get_racks_by_ids(self, rack_ids: list) -> List[Rack]:
        q = select(RackModel).where(RackModel.id.in_(rack_ids))

        result = self.session.execute(q)

        models = result.scalars().all()

        racks = [
            Rack(
                id=m.id,
                name=m.name,
                description=m.description,
                serial_number=m.serial_number,
                max_power_watts=m.max_power_watts,
                total_units=m.total_units,
            )
            for m in models
        ]

        return racks
