from worker import celery


def test_run_training(client, mock_celery_and_redis, input_train_data):
    response = client.post("api/train/run", json=input_train_data.model_dump())
    assert response.status_code == 200
    result = response.json()
    assert result["task_id"] == "mock_task_id"
    assert result["status"] == "success"


def test_status_success(client, mock_celery_and_redis):
    response = client.get("api/train/check", params={"task_id": "mock_task_id"})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["id"] == "mock_task_id"
    assert json_response["status"] == "running"
    assert "time_start" in json_response


def test_status_no_task_id(client, mock_celery_and_redis):
    response = client.get("api/train/check")
    assert response.status_code == 422
