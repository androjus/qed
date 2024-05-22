from pydantic import BaseModel


class PredictInput(BaseModel):
    data: list[list[float]]


class PredictResult(BaseModel):
    result: list[float]
