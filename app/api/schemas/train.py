from typing import Optional

from custom_types import MATRIX
from pydantic import BaseModel


class TrainData(BaseModel):
    data: MATRIX
    L: int
    K: int


class TrainRun(BaseModel):
    status: str
    task_id: str
    error: Optional[str] = None


class TrainStatus(BaseModel):
    id: str
    status: str
    time_start: Optional[float] = None
    time_end: Optional[float] = None
    error: Optional[str] = None
