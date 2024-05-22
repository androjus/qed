import os
import pickle

import numpy as np
from api.schemas.train import TrainData
from celery import result
from config import Config
from infrastructure.tasks import training


class ModelsMeta(type):
    """Models Meta Class. Only one instance of Model should exist."""

    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__call__(*args, **kwargs)
            cls._instance = instance

        return cls._instance


class Representativeness(metaclass=ModelsMeta):
    def __init__(self) -> None:
        self.models = self._load_model()

    def _load_model(self):
        if os.path.isfile(Config.MODEL_PATH):
            return pickle.load(open(Config.MODEL_PATH, "rb"))
        else:
            return None

    def train(self, data: TrainData) -> result.AsyncResult:
        task = training.delay(data.dict())
        return task

    def predict(self, X: list[list[float]]) -> list[float]:
        self.models = self._load_model()
        predictions = np.array([model.predict(X) for model in self.models])
        return predictions.mean(axis=0).tolist()
