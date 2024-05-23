import pickle

from infrastructure.tasks import train_representativeness


def test_train_representativeness(serialized_array, input_train_data):
    dataset = serialized_array
    K = input_train_data.K

    trained_model = train_representativeness(dataset, K)
    loaded_model = pickle.loads(trained_model)

    assert loaded_model is not None
