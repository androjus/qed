import json

import numpy as np
from custom_types import MATRIX


def split_data(data: MATRIX, L: int) -> MATRIX:
    np.random.shuffle(data)
    split_data = np.array_split(data, L)
    return [sub_array.tolist() for sub_array in split_data]


def serialize_array(array: np.ndarray) -> str:
    return json.dumps(array.tolist())


def deserialize_array(array_json: str) -> np.ndarray:
    return np.array(json.loads(array_json))
