import json

import numpy as np
from infrastructure.utils import deserialize_array, serialize_array, split_data


def test_split_data(data_list):
    L = 2
    split_result = split_data(data_list, L)

    assert len(split_result) == L
    assert sum(len(part) for part in split_result) == len(data_list)

    concatenated = np.concatenate(split_result)
    assert set(map(tuple, concatenated)) == set(map(tuple, data_list))


def test_serialize_array(array):
    serialized = serialize_array(array)

    deserialized = json.loads(serialized)
    assert deserialized == array.tolist()

    assert isinstance(serialized, str)


def test_deserialize_array(serialized_array, array):
    deserialized = deserialize_array(serialized_array)

    assert isinstance(deserialized, np.ndarray)

    assert np.array_equal(deserialized, array)


def test_serialize_deserialize_array(array):
    serialized = serialize_array(array)
    deserialized = deserialize_array(serialized)

    assert np.array_equal(array, deserialized)
