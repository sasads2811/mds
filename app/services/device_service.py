from app.domain.device.entity import Device
from app.infrastructure.repositories.device_repo import DeviceRepository


class DeviceService:

    def __init__(self, repo: DeviceRepository):
        self.repo = repo

    def list_devices(self):
        return self.repo.get_all()

    def create_device(self, data: dict):
        device = Device(
            id=None,
            name=data["name"],
            description=data.get("description"),
            serial_number=data["serial_number"],
            rack_units=data["rack_units"],
            power_watts=data["power_watts"],
        )

        device.validate()

        return self.repo.create(device)