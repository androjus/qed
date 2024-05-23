import json
from datetime import datetime
from unittest.mock import MagicMock

import numpy as np
import pytest
from api.schemas.predict import PredictInput
from api.schemas.train import TrainData
from fastapi.testclient import TestClient
from main import app
from worker import celery, redis_instance


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def mock_representativeness(monkeypatch):
    class MockRepresentativeness:
        trained = True
        mock_id = "mock_task_id"

        def train(self, input_data):
            self.trained = True
            mock_task = MagicMock()
            mock_task.id = self.mock_id
            return mock_task

        def predict(self, data):
            if not self.trained:
                raise RuntimeError("No trained model")
            return [0.68]

    mock = MockRepresentativeness()
    monkeypatch.setattr(
        "infrastructure.representativeness.Representativeness.train",
        mock.train,
    )
    monkeypatch.setattr(
        "infrastructure.representativeness.Representativeness.predict",
        mock.predict,
    )

    return mock


@pytest.fixture(autouse=True)
def mock_celery_and_redis(monkeypatch):
    class MockAsyncResult:
        def __init__(self, task_id):
            self.task_id = task_id
            self.state = "SUCCESS"
            self.info = {"data_created": datetime.now()}
            self.date_done = None

        def successful(self):
            return self.state == "SUCCESS"

        def get(self):
            return self.info["data_created"], None

    def mock_active_tasks(task):
        return {"task_ongoing": [{"id": "123", "name": "Task 1"}]}

    monkeypatch.setattr("worker.celery.control.inspect.active", mock_active_tasks)
    monkeypatch.setattr(celery, "AsyncResult", MockAsyncResult)
    monkeypatch.setattr(redis_instance, "get", lambda x: "mock_task_id")


@pytest.fixture(scope="module")
def input_data_predict():
    return PredictInput(data=[[1, 1, 1]])


@pytest.fixture(scope="module")
def data_list():
    return [
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 9.0],
        [10.0, 11.0, 12.0],
    ]


@pytest.fixture(scope="module")
def serialized_array():
    return json.dumps([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])


@pytest.fixture(scope="module")
def array():
    return np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])


@pytest.fixture(scope="module")
def input_train_data():
    return TrainData(data=[[1, 2, 3], [4, 5, 6]], K=2, L=2)
