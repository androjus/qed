from api.routers import api_router
from fastapi import FastAPI

app = FastAPI(
    title="QED recruitment task",
)

app.include_router(api_router)
