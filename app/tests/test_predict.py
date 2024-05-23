def test_run_predict_success(client, input_data_predict, mock_representativeness):
    response = client.post("api/predict/use", json=input_data_predict.model_dump())
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert "result" in result


def test_run_predict_no_model(client, input_data_predict, mock_representativeness):
    mock_representativeness.trained = False
    response = client.post("api/predict/use", json=input_data_predict.model_dump())
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "error"
    assert "No trained model" in result["error"]


def test_run_predict_exception(client, input_data_predict, monkeypatch):
    monkeypatch.setattr(
        "infrastructure.representativeness.Representativeness.predict",
        lambda self, data: 1 / 0,
    )
    response = client.post("api/predict/use", json=input_data_predict.model_dump())
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "error"
    assert "division by zero" in result["error"]
