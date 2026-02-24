from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.infrastructure.db.models import DeviceModel, RackDeviceModel, RackModel
from app.domain.device.entity import Device
from app.domain.rack.entity import Rack
from app.domain.placement.entity import RackDevice
from app.infrastructure.db.base import Base
from app.main import app
from app.api.dependencies import get_db
from app.infrastructure.repositories.device_repo import DeviceRepository
from app.infrastructure.repositories.rack_repo import RackRepository

ADMIN_DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5444/mydatabase"
TEST_DB_NAME = "test_db"
TEST_DB_URL = f"postgresql+psycopg://postgres:postgres@localhost:5444/{TEST_DB_NAME}"


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    admin_engine = create_engine(ADMIN_DB_URL, isolation_level="AUTOCOMMIT")

    with admin_engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME}"))

    yield

    with admin_engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))

    admin_engine.dispose()


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DB_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db(engine):
    connection = engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(bind=connection)
    session = TestingSessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def device_repository(db):
    return DeviceRepository(db)


@pytest.fixture(scope="function")
def rack_repository(db):
    return RackRepository(db)


@pytest.fixture(scope="function")
def device(db):
    model = DeviceModel(
        id=uuid4(),
        name="Device Name",
        description="Device Description",
        serial_number="678267GYgyg6767",
        power_watts=100,
        rack_units=5,
    )
    db.add(model)
    db.commit()
    db.refresh(model)

    return Device(
        id=model.id,
        name=model.name,
        description=model.description,
        serial_number=model.serial_number,
        power_watts=model.power_watts,
        rack_units=model.rack_units,
    )


@pytest.fixture(scope="function")
def rack(db):
    model = RackModel(
        id=uuid4(),
        name="Rack Name",
        description="Rack Description",
        serial_number="678267GYgyg6767",
        max_power_watts=1000,
        total_units=50,
    )
    db.add(model)
    db.commit()
    db.refresh(model)

    return Rack(
        id=model.id,
        name=model.name,
        description=model.description,
        serial_number=model.serial_number,
        max_power_watts=model.max_power_watts,
        total_units=model.total_units,
    )


@pytest.fixture(scope="function")
def rack_device(db, rack, device):
    model = RackDeviceModel(
        id=uuid4(),
        rack_id=rack.id,
        device_id=device.id,
        start_unit=1,
        end_unit=1 + device.rack_units,
    )
    db.add(model)
    db.commit()
    db.refresh(model)

    return RackDevice(
        id=model.id,
        rack_id=model.rack_id,
        device_id=model.device_id,
        start_unit=model.start_unit,
        end_unit=model.end_unit,
    )
