import json

import numpy as np


def split_data(data: list[list[float]], L: int):
    np.random.shuffle(data)
    split_data = np.array_split(data, L)
    return split_data


def serialize_array(array):
    return json.dumps(array.tolist())


def deserialize_array(array_json):
    return np.array(json.loads(array_json))