import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.api.dtos.device_dto import DeviceResponse, DeviceCreate, EditDevice
from app.api.dependencies import get_db
from app.infrastructure.repositories.device_repo import DeviceRepository
from app.services.device_service import DeviceService

device_router = APIRouter(prefix="/device", tags=["Devices"])


def get_service(db: Session = Depends(get_db)):
    repo = DeviceRepository(db)
    return DeviceService(repo)


@device_router.get("/", response_model=list[DeviceResponse])
def get_devices(service: DeviceService = Depends(get_service)):
    return service.list_devices()


@device_router.post("/create", response_model=DeviceResponse)
def create_device(data: DeviceCreate, service: DeviceService = Depends(get_service)):
    try:
        return service.create_device(
            name=data.name,
            description=data.description,
            serial_number=data.serial_number,
            rack_units=data.rack_units,
            power_watts=data.power_watts,
        )
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@device_router.put("/{device_id}", response_model=DeviceResponse)
def edit_device(
    device_id: uuid.UUID,
    data: EditDevice,
    service: DeviceService = Depends(get_service),
):
    try:
        return service.edit_device(
            id=device_id,
            name=data.name,
            description=data.description,
            rack_units=data.rack_units,
            serial_number=data.serial_number,
            power_watts=data.power_watts,
        )
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
