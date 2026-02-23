import uuid
from dataclasses import dataclass


@dataclass
class Rack:
    id: uuid.UUID | None
    name: str
    description: str
    serial_number: str
    total_units: int
    max_power_watts: int

    def validate(self):
        if self.total_units <= 0:
            raise ValueError("Rack units must be positive")

        if self.max_power_watts <= 0:
            raise ValueError("Power must be positive")

    def update(
        self,
        name=None,
        description=None,
        total_units=None,
        max_power_watts=None,
        serial_number=None,
    ):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if total_units is not None:
            self.total_units = total_units
        if max_power_watts is not None:
            self.max_power_watts = max_power_watts
        if serial_number is not None:
            self.serial_number = serial_number

    def find_free_slot(self, occupied_ranges, device_size):
        occupied_ranges.sort(key=lambda x: x[0])
        current_unit = 1

        for start, end in occupied_ranges:
            if current_unit + device_size - 1 < start:
                return current_unit
            current_unit = end + 1

        if current_unit + device_size - 1 > self.total_units:
            raise ValueError("No free space in rack")

        return current_unit
