from api.schemas.predict import PredictInput, PredictResult
from fastapi import APIRouter
from infrastructure.representativeness import Representativeness

router = APIRouter(
    prefix="/predict",
)

model = Representativeness()


@router.post(
    "/get",
    name="Train model",
    description="Training of the model using the provided data",
)
def run_predict(input_data: PredictInput) -> PredictResult:
    return PredictResult(result=model.predict(input_data.data))
