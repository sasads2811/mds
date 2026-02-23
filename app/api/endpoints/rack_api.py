import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.api.dependencies import get_db
from app.infrastructure.repositories.rack_repo import RackRepository
from app.services.rack_service import RackService
from app.api.dtos.rack_dto import RackCreate, RackResponse, EditRack


def get_service(db: Session = Depends(get_db)):
    repo = RackRepository(db)
    return RackService(repo)


rack_router = APIRouter(
    prefix="/rack",
    tags=["Racks"],
)


@rack_router.get("", response_model=list[RackResponse])
def get_all_racks(service: RackService = Depends(get_service)):
    try:
        return service.get_all_racks()
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@rack_router.get("/{rack_id}", response_model=RackResponse)
def get_rack(rack_id: uuid.UUID, service: RackService = Depends(get_service)):
    try:
        return service.get_rack(rack_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@rack_router.post("/create", response_model=RackResponse)
def create_rack(data: RackCreate, service: RackService = Depends(get_service)):
    try:
        return service.create_rack(
            name=data.name,
            description=data.description,
            serial_number=data.serial_number,
            max_power_watts=data.max_power_watts,
            total_units=data.total_units,
        )
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@rack_router.put("/{rack_id}", response_model=RackResponse)
def update_rack(
    rack_id: uuid.UUID, data: EditRack, service: RackService = Depends(get_service)
):
    try:
        return service.update_rack(
            id=rack_id,
            name=data.name,
            description=data.description,
            serial_number=data.serial_number,
            total_units=data.total_units,
            max_power_watts=data.max_power_watts,
        )
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
