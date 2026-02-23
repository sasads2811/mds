from dataclasses import dataclass
from uuid import UUID


@dataclass
class RackDevice:
    id: UUID | None
    rack_id: UUID
    device_id: UUID
    start_unit: int
    end_unit: int

    @classmethod
    def create(
        cls,
        rack_id: UUID,
        device_id: UUID,
        start_unit: int,
        size_units: int,
        total_units: int,
    ):
        """
        Factory method sa validacijom:
        - proverava da li uređaj izlazi iz granica rack-a
        """
        end_unit = start_unit + size_units - 1
        if start_unit < 1 or end_unit > total_units:
            raise ValueError("Device exceeds rack boundaries")
        return cls(
            rack_id=rack_id,
            device_id=device_id,
            start_unit=start_unit,
            end_unit=end_unit,
        )
