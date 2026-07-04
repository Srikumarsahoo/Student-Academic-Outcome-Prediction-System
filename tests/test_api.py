from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "Running"


def test_prediction_page_renders():
    response = client.get("/predict")

    assert response.status_code == 200
    assert "Predict a student outcome" in response.text
