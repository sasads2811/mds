from uuid import uuid4
from app.domain.rack.entity import Rack
import pytest


def test_get_rack_by_id(rack_repository, rack, rack_device):
    data = rack_repository.get_rack_by_id(rack.id)

    assert data.id == rack.id


def test_get_device_by_id(rack_repository, device):
    data = rack_repository.get_device_by_id(device.id)

    assert data.id == device.id


def test_get_all_racks(rack_repository, rack):
    data = rack_repository.get_all()

    assert len(data) > 0
    assert data[0].id == rack.id


def test_create_rack(rack_repository):
    rack = Rack(
        id=uuid4(),
        name="Rack 1",
        description="Rack 1",
        serial_number="dsasdas",
        max_power_watts=1000,
        total_units=50,
    )

    data = rack_repository.create(rack)

    assert data.id == rack.id


def test_save_rack(rack_repository, rack):
    rack = Rack(
        id=rack.id,
        name="Edit 1",
        description="Rack 1",
        serial_number="dsasdas",
        max_power_watts=1000,
        total_units=50,
    )

    data = rack_repository.save(rack)
    assert data.name == rack.name


def test_create_rack_device(rack_repository, rack, device):
    data = rack_repository.create_rack_device(
        rack_id=rack.id,
        device_id=device.id,
        start_unit=1,
        end_unit=1 + device.rack_units,
    )

    assert data is not None


def test_get_rack_device_by_rack_and_device_id(rack_repository, rack_device):
    data = rack_repository.get_rack_device_by_rack_and_device_id(
        rack_id=rack_device.rack_id, device_id=rack_device.device_id
    )

    assert data.id == rack_device.id


def test_get_devices_by_ids(rack_repository, device):
    data = rack_repository.get_devices_by_ids([device.id])

    assert len(data) > 0
    assert data[0].id == device.id


def test_get_racks_by_ids(rack_repository, rack):
    data = rack_repository.get_racks_by_ids([rack.id])

    assert len(data) > 0
    assert data[0].id == rack.id
