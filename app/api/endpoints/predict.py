from api.schemas.predict import PredictInput, PredictResult
from fastapi import APIRouter
from infrastructure.representativeness import Representativeness

router = APIRouter(
    prefix="/predict",
)

model = Representativeness()


@router.post(
    "/use",
    name="Predict",
    description="Prediction using a previously trained model.",
)
def run_predict(input_data: PredictInput) -> dict:
    try:
        return PredictResult(
            status="success", result=model.predict(input_data.data)
        ).model_dump(exclude_defaults=True, exclude_none=True)
    except Exception as e:
        return PredictResult(status="error", error=str(e)).model_dump(
            exclude_defaults=True, exclude_none=True
        )
