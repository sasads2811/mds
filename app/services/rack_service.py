import uuid

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
