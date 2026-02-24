import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.api.dependencies import get_db
from app.infrastructure.repositories.rack_repo import RackRepository
from app.services.rack_service import RackService
from app.api.dtos.rack_dto import (
    RackCreate,
    RackResponse,
    EditRack,
    RackDeviceResponse,
    AddDeviceRequest,
    BalanceRequest,
)


def get_service(db: Session = Depends(get_db)):
    repo = RackRepository(db)
    return RackService(repo)


rack_router = APIRouter(
    prefix="/rack",
    tags=["Racks"],
)


@rack_router.get("", response_model=list[RackResponse])
def get_all_racks(service: RackService = Depends(get_service)):
    """
    ## Method is used for getting all racks.

    ### Returns:
    - **Success**: Returns list of racks.
    - **Error**: A JSON error object with HTTP status code 400.
    """

    try:
        return service.get_all_racks()
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@rack_router.get("/{rack_id}", response_model=RackResponse)
def get_rack(rack_id: uuid.UUID, service: RackService = Depends(get_service)):
    """
    ## Method is used for getting rack details.

    ### Parameters:
    - `rack_id`: The id of rack.


    ### Returns:
    - **Success**: Returns rack details.
    - **Error**: A JSON error object with HTTP status code 400.
    """

    try:
        return service.get_rack(rack_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@rack_router.post("/create", response_model=RackResponse)
def create_rack(data: RackCreate, service: RackService = Depends(get_service)):
    """
    ## Method is used for creating rack.

    ### Parameters:
    - `name`: The name of rack.
    - `description`: The description of rack.
    - `serial_number`: The serial number of rack.
    - `total_units`: The number of rack units.
    - `max_power_watts`: The max power watts.

    ### Returns:
    - **Success**: Returns rack details.
    - **Error**: A JSON error object with HTTP status code 400.
    """

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


@rack_router.post("/balance")
def balance(data: BalanceRequest, service: RackService = Depends(get_service)):
    """
    ## Method is used for providing balance for given devices and racks.

     ### Parameters:
    - `devices`: The list of ids of devices.
    - `racks`: The list of ids of racks.

    ### Returns:
    - **Success**: Returns balance for given devices and racks.
    - **Error**: A JSON error object with HTTP status code 400.
    """

    try:
        return service.balance_rack(device_ids=data.devices, rack_ids=data.racks)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@rack_router.put("/{rack_id}", response_model=RackResponse)
def update_rack(
    rack_id: uuid.UUID, data: EditRack, service: RackService = Depends(get_service)
):
    """
    ## Method is used for creating rack.

    ### Parameters:
    - `rack_id`: The id of rack.
    - `name`: The name of rack.
    - `description`: The description of rack.
    - `serial_number`: The serial number of rack.
    - `total_units`: The number of rack units.
    - `max_power_watts`: The max power watts.

    ### Returns:
    - **Success**: Returns rack details.
    - **Error**: A JSON error object with HTTP status code 400.
    """

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


@rack_router.post("/{rack_id}", response_model=RackDeviceResponse)
def add_device(
    rack_id: uuid.UUID,
    data: AddDeviceRequest,
    service: RackService = Depends(get_service),
):
    """
    ## Method is used for adding device to rack.

    ### Parameters:
    - `rack_id`: The id of rack.
    - `device_id`: The id of device.


    ### Returns:
    - **Success**: Returns rack device placement details.
    - **Error**: A JSON error object with HTTP status code 400.
    """

    try:
        return service.add_device_to_rack(rack_id, data.device_id)

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
