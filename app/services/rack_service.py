import uuid

from app.domain.device.entity import Device
from app.domain.rack.entity import Rack
from app.infrastructure.repositories.rack_repo import RackRepository


class RackService:

    def __init__(self, repo: RackRepository):
        self.repo = repo

    def get_all_racks(self):
        return self.repo.get_all()

    def get_rack(self, rack_id: uuid.UUID):
        rack = self.repo.get_rack_by_id(rack_id=rack_id)
        if not rack:
            raise ValueError(f"Rack with id {rack_id} not found")
        return rack

    def create_rack(
        self,
        name: str,
        description: str,
        total_units: int,
        max_power_watts: int,
        serial_number: str,
    ):
        rack = Rack(
            id=None,
            name=name,
            description=description,
            serial_number=serial_number,
            total_units=total_units,
            max_power_watts=max_power_watts,
        )

        rack.validate()

        return self.repo.create(rack)

    def update_rack(
        self,
        id: uuid.UUID,
        name: str,
        description: str,
        total_units: int,
        max_power_watts: int,
        serial_number: str,
    ):
        result = self.repo.get_rack_by_id(rack_id=id)
        if not result:
            raise ValueError(f"Device with id {id} not found")

        rack = Rack(
            id=result.id,
            name=result.name,
            description=result.description,
            serial_number=result.serial_number,
            total_units=result.total_units,
            max_power_watts=result.max_power_watts,
        )

        rack.update(
            name=name,
            description=description,
            total_units=total_units,
            max_power_watts=max_power_watts,
            serial_number=serial_number,
        )
        rack.validate()

        return self.repo.save(rack)

    def add_device_to_rack(self, rack_id: uuid.UUID, device_id: uuid.UUID):
        rack = self.repo.get_rack_by_id(rack_id=rack_id)
        if not rack:
            raise ValueError(f"Rack with id {rack_id} not found")

        device = self.repo.get_device_by_id(device_id=device_id)
        if not device:
            raise ValueError(f"Device with id {device_id} not found")

        rack_device = self.repo.get_rack_device_by_rack_and_device_id(
            rack_id=rack_id, device_id=device_id
        )
        if rack_device:
            raise ValueError(f"Device with id {device_id} already exists in rack")

        device = Device(
            id=device_id,
            name=device.name,
            description=device.description,
            serial_number=device.serial_number,
            rack_units=device.rack_units,
            power_watts=device.power_watts,
        )

        placements = self.repo.get_rack_devices(rack_id)

        occupied_ranges = [(p.start_unit, p.end_unit) for p in placements]

        rack = Rack(
            id=rack_id,
            name=rack.name,
            description=rack.description,
            serial_number=rack.serial_number,
            total_units=rack.total_units,
            max_power_watts=rack.max_power_watts,
        )
        start_unit = rack.find_free_slot(
            occupied_ranges=occupied_ranges, device_size=device.rack_units
        )

        end_unit = start_unit + device.rack_units - 1

        total_power = sum(p.device.power_watts for p in placements)
        if total_power + device.power_watts > rack.max_power_watts:
            raise ValueError("Rack power capacity exceeded")

        return self.repo.create_rack_device(
            rack_id=rack_id,
            device_id=device_id,
            start_unit=start_unit,
            end_unit=end_unit,
        )
