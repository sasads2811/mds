import uuid

from app.domain.device.entity import Device
from app.infrastructure.repositories.device_repo import DeviceRepository


class DeviceService:

    def __init__(self, repo: DeviceRepository):
        self.repo = repo

    def list_devices(self):
        return self.repo.get_all()

    def create_device(
        self,
        name: str,
        description: str,
        rack_units: int,
        power_watts: int,
        serial_number: str,
    ):
        device = Device(
            id=None,
            name=name,
            description=description,
            serial_number=serial_number,
            rack_units=rack_units,
            power_watts=power_watts,
        )

        device.validate()

        return self.repo.create(device)

    def edit_device(
        self,
        id: uuid.UUID,
        name: str,
        description: str,
        rack_units: int,
        power_watts: int,
        serial_number: str,
    ):
        result = self.repo.get_device_by_id(device_id=id)
        if not result:
            raise ValueError(f"Device with id {id} not found")

        device = Device(
            id=result.id,
            name=result.name,
            description=result.description,
            serial_number=result.serial_number,
            rack_units=result.rack_units,
            power_watts=result.power_watts,
        )

        device.update(
            name=name,
            description=description,
            rack_units=rack_units,
            power_watts=power_watts,
            serial_number=serial_number,
        )
        device.validate()

        return self.repo.save(device)
