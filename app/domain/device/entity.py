import uuid
from dataclasses import dataclass


@dataclass
class Device:
    id: uuid.UUID | None
    name: str
    description: str | None
    serial_number: str
    rack_units: int
    power_watts: int

    def validate(self):
        if self.rack_units <= 0:
            raise ValueError("Rack units must be positive")

        if self.power_watts <= 0:
            raise ValueError("Power must be positive")

    def update(
        self,
        name=None,
        description=None,
        rack_units=None,
        power_watts=None,
        serial_number=None,
    ):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if rack_units is not None:
            self.rack_units = rack_units
        if power_watts is not None:
            self.power_watts = power_watts
        if serial_number is not None:
            self.serial_number = serial_number
