from fastapi.testclient import TestClient
from src.app import app

def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

def test_prediction_success():
    with TestClient(app) as client:
        payload = {
            "temperature_celsius": 14.0,
            "hour_of_day": 12,
            "day_of_week": 2,
            "is_holiday": 0
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "predicted_load_mw" in data
        assert data["predicted_load_mw"] > 0

def test_validation_rejection_negative_hour():
    with TestClient(app) as client:
        bad_payload = {
            "temperature_celsius": 14.0,
            "hour_of_day": -1,
            "day_of_week": 2,
            "is_holiday": 0
        }
        response = client.post("/predict", json=bad_payload)
        assert response.status_code == 422