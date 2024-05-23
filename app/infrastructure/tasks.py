import pickle
from datetime import datetime, timezone
from typing import Optional, Tuple

from api.schemas.train import TrainData
from celery import group
from celery.result import allow_join_result
from config import Config
from infrastructure.utils import deserialize_array, serialize_array, split_data
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import NearestNeighbors
from worker import celery


@celery.task(name="train_model", bind=True)
def training(self, data: dict) -> Tuple[datetime, Optional[str]]:
    try:
        data_created = datetime.now(timezone.utc)
        self.update_state(
            state="PROGRESS", meta={"data_created": data_created}
        )
        data_obj = TrainData(**data)
        data_obj.data = split_data(data_obj.data, data_obj.L)
        tasks = [
            train_representativeness.s(serialize_array(dataset), data_obj.K)
            for dataset in data_obj.data
        ]
        result_group = group(tasks)()
        with allow_join_result():
            results = result_group.get()
            deserialized_models = [pickle.loads(model) for model in results]
            with open(Config.MODEL_PATH, "wb") as f:
                pickle.dump(deserialized_models, f)
        return data_created, None
    except Exception as e:
        return data_created, str(e)


@celery.task()
def train_representativeness(dataset: str, K: int):
    subset = deserialize_array(dataset)
    nbrs = NearestNeighbors(n_neighbors=K, algorithm="auto").fit(subset)
    distances, _ = nbrs.kneighbors(subset)
    mean_distances = distances.mean(axis=1)
    representativeness = 1 / (1 + mean_distances)
    model = LinearRegression().fit(subset, representativeness)
    return pickle.dumps(model)
