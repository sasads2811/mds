from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.api.dtos.device_dto import (
    DeviceResponse,
)
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
