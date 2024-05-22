from api.endpoints import predict, train
from fastapi import APIRouter

api_router = APIRouter(
    prefix="/api",
    tags=[
        "API",
    ],
)

api_router.include_router(train.router)  # type: ignore
api_router.include_router(predict.router)  # type: ignore
