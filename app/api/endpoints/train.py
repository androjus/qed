from datetime import datetime

from api.schemas.train import TrainData, TrainRun, TrainStatus
from fastapi import APIRouter, HTTPException
from infrastructure.representativeness import Representativeness
from worker import REDIS_TASK_KEY, celery, redis_instance

router = APIRouter(
    prefix="/train",
)

model = Representativeness()


@router.post(
    "/run",
    name="Train model",
    description="Training of the model using the provided data",
)
async def run_training(input_data: TrainData) -> TrainRun:
    task = model.train(input_data)
    return TrainRun(task_id=task.id)


@router.get("/check")
def status(task_id) -> dict:
    task_id = task_id or redis_instance.get(REDIS_TASK_KEY)
    if task_id is None:
        raise HTTPException(
            status_code=400, detail=f"Could not determine task {task_id}"
        )
    task_result = celery.AsyncResult(task_id)
    if task_result.date_done:
        date_created, error = task_result.get()
        if error:
            result = TrainStatus(
                id=task_result.task_id,
                status="failed",
                time_start=datetime.timestamp(date_created),
                time_end=datetime.timestamp(task_result.date_done),
                error=error,
            )
        elif task_result.successful():
            result = TrainStatus(
                id=task_result.task_id,
                status="completed",
                time_start=datetime.timestamp(date_created),
                time_end=datetime.timestamp(task_result.date_done),
            )
    else:
        result = TrainStatus(
            id=task_result.task_id,
            status="running",
            time_start=datetime.timestamp(
                task_result.info.get("data_created")
            ),
        )

    return result.model_dump(exclude_defaults=True, exclude_none=True)
