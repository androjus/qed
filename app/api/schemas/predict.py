from typing import Optional

from custom_types import MATRIX, VECTOR
from pydantic import BaseModel


class PredictInput(BaseModel):
    data: MATRIX


class PredictResult(BaseModel):
    status: str
    result: Optional[VECTOR] = None
    error: Optional[str] = None
