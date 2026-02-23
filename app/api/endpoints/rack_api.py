from fastapi import APIRouter

rack_router = APIRouter(
    prefix="/rack",
    tags=["Rack"],
)