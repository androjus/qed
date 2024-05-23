from typing import Optional

from pydantic import BaseModel


class PredictInput(BaseModel):
    data: list[list[float]]


class PredictResult(BaseModel):
    status: str
    result: Optional[list[float]] = None
    error: Optional[str] = None
