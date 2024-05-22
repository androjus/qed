from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TrainData(BaseModel):
    data: list[list[float]]
    L: int
    K: int


class TrainRun(BaseModel):
    task_id: str


class TrainStatus(BaseModel):
    id: str
    status: str
    time_start: Optional[float] = None
    time_end: Optional[float] = None
    error: Optional[str] = None