import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from app.services.rack_service import RackService
from app.domain.device.entity import Device
from app.domain.rack.entity import Rack


def test_balance_rack_success():
    mock_repo = MagicMock()

    device = Device(
        id=uuid4(),
        name="Device",
        description="",
        serial_number="SN1",
        power_watts=100,
        rack_units=2,
    )

    rack = Rack(
        id=uuid4(),
        name="Rack",
        description="",
        serial_number="RSN1",
        max_power_watts=500,
        total_units=10,
    )

    mock_repo.get_devices_by_ids.return_value = [device]
    mock_repo.get_racks_by_ids.return_value = [rack]

    service = RackService(mock_repo)

    result = service.balance_rack([device.id], [rack.id])

    assert rack.id in result
    assert result[rack.id]["current_power"] == 100


def test_balance_rack_device_not_found():
    mock_repo = MagicMock()

    device_id = uuid4()
    rack_id = uuid4()

    mock_repo.get_devices_by_ids.return_value = []
    mock_repo.get_racks_by_ids.return_value = []

    service = RackService(mock_repo)

    with pytest.raises(ValueError) as exc:
        service.balance_rack([device_id], [rack_id])

    assert "Device not found" in str(exc.value)


def test_balance_rack_rack_not_found():
    mock_repo = MagicMock()

    device = Device(
        id=uuid4(),
        name="Device",
        description="",
        serial_number="SN1",
        power_watts=100,
        rack_units=2,
    )

    mock_repo.get_devices_by_ids.return_value = [device]
    mock_repo.get_racks_by_ids.return_value = []

    service = RackService(mock_repo)

    with pytest.raises(ValueError) as exc:
        service.balance_rack([device.id], [uuid4()])

    assert "Rack not found" in str(exc.value)


def test_balance_rack_power_exceeded():
    mock_repo = MagicMock()

    device = Device(
        id=uuid4(),
        name="Device",
        description="",
        serial_number="SN1",
        power_watts=600,
        rack_units=2,
    )

    rack = Rack(
        id=uuid4(),
        name="Rack",
        description="",
        serial_number="RSN1",
        max_power_watts=500,
        total_units=10,
    )

    mock_repo.get_devices_by_ids.return_value = [device]
    mock_repo.get_racks_by_ids.return_value = [rack]

    service = RackService(mock_repo)

    with pytest.raises(ValueError) as exc:
        service.balance_rack([device.id], [rack.id])

    assert "Rack power capacity exceeded" in str(exc.value)
