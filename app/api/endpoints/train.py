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
async def run_training(input_data: TrainData) -> dict:
    task_status = celery.control.inspect().active()

    if task_status:
        for _, tasks in task_status.items():
            for task in tasks:
                if task["name"] == "train_model":
                    result = TrainRun(
                        task_id=task["id"],
                        status="error",
                        error="Training is currently ongoing. The next one can be ordered after the current one ends. The training status can be checked using the returned ID.",
                    )
                    return result

    task = model.train(input_data)
    return TrainRun(task_id=task.id, status="success").model_dump(
        exclude_defaults=True, exclude_none=True
    )


@router.get(
    "/check",
    name="Training status",
    description="Training status under a given ID",
)
def status(task_id: str) -> dict:
    task_id = task_id or redis_instance.get(REDIS_TASK_KEY)
    if (
        task_id is None
        or redis_instance.get(f"celery-task-meta-{task_id}") is None
    ):
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
