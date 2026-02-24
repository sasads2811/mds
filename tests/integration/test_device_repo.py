import pytest
from app.domain.device.entity import Device
from uuid import uuid4


def test_get_device_by_id(device_repository, device):
    data = device_repository.get_device_by_id(device.id)
    assert data.id == device.id


def test_get_all_devices(device_repository, device):
    data = device_repository.get_all()

    assert len(data) > 0
    assert data[0].id == device.id


def test_create_device(device_repository):
    device = Device(
        id=uuid4(),
        name="Device Name",
        description="Device Description",
        serial_number="Device Serial Number",
        power_watts=10,
        rack_units=50,
    )
    data = device_repository.create(device)
    assert data.id == device.id


def test_save_device(device_repository, device):
    model = Device(
        id=device.id,
        name="Device Name",
        description="Device Description",
        serial_number="Device Serial Number",
        power_watts=10,
        rack_units=50,
    )
    data = device_repository.save(model)
    assert data.id == device.id
