import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_pagination import add_pagination
from starlette import status


from app.api.endpoints.device_api import device_router
from app.api.endpoints.rack_api import rack_router

app = FastAPI(
    title="MDS",
)


app.include_router(
    device_router,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
)
app.include_router(
    rack_router,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

add_pagination(app)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
