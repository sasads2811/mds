from dataclasses import dataclass
from typing import List
from uuid import UUID
from app.domain.rack.entity import Rack
from app.domain.device.entity import Device


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

    @staticmethod
    def balance_devices(devices: List[Device], racks: List[Rack]):

        devices = sorted(devices, key=lambda d: d.power_watts, reverse=True)

        rack_state = {
            r.id: {"max_power": r.max_power_watts, "current_power": 0, "devices": []}
            for r in racks
        }

        for device in devices:
            possible_racks = [
                r_id
                for r_id, r in rack_state.items()
                if r["current_power"] + device.power_watts <= r["max_power"]
            ]

            if not possible_racks:
                raise ValueError(
                    f"Nema mesta za uređaj {device['id']} ({device['power']}W)"
                )

            best_rack = min(
                possible_racks,
                key=lambda r_id: (
                    rack_state[r_id]["current_power"] / rack_state[r_id]["max_power"]
                ),
            )

            rack_state[best_rack]["devices"].append(device)
            rack_state[best_rack]["current_power"] += device.power_watts

        for r_id, r in rack_state.items():
            r["utilization_percent"] = round(
                (r["current_power"] / r["max_power"]) * 100, 2
            )

        return rack_state
