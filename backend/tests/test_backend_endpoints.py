from fastapi.testclient import TestClient
from backend.app.main_api import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_patients():
    response = client.get("/api/patients")
    assert response.status_code == 200
    assert "patients" in response.json()

def test_predict_endpoint():
    payload = {
        "patient_id": "GT-PATIENT-001",
        "recent_glucose": [140.0, 142.0, 144.5, 147.0],
        "current_steps": 150,
        "current_sleep": 8.0
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    assert "predicted_glucose_30min" in response.json()

def test_scenario_endpoint():
    payload = {
        "patient_id": "GT-PATIENT-001",
        "baseline_glucose": 150.0,
        "delta_carbs_g": 45.0,
        "delta_activity_minutes": 30.0,
        "delta_sleep_hours": 0.0
    }
    response = client.post("/api/scenario", json=payload)
    assert response.status_code == 200
    assert "scenario_forecast" in response.json()