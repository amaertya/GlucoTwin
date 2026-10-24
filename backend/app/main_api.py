from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.app.schemas import PredictRequest, PredictResponse, ScenarioRequest, ScenarioResponse
from backend.app.services.twin_engine import twin_engine
from backend.app.settings import METRICS_PATH
import json

app = FastAPI(
    title="GlucoTwin API",
    version="1.0.0",
    description="Backend API for GlucoTwin Personalised Glucose Response Digital Twin"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": twin_engine.model is not None,
        "version": "1.0.0"
    }

@app.get("/api/patients")
def get_patients():
    patients = twin_engine.df_patients.to_dict(orient="records")
    return {"patients": patients}

@app.get("/api/patients/{patient_id}")
def get_patient(patient_id: str):
    row = twin_engine.df_patients[twin_engine.df_patients["patient_id"] == patient_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Patient not found")
    return row.iloc[0].to_dict()

@app.get("/api/patients/{patient_id}/observations")
def get_observations(patient_id: str, limit: int = 40):
    obs = twin_engine.df_obs[twin_engine.df_obs["patient_id"] == patient_id]
    if obs.empty:
        raise HTTPException(status_code=404, detail="No observations found for patient")
    return {"observations": obs.tail(limit).to_dict(orient="records")}

@app.post("/api/predict", response_model=PredictResponse)
def predict_glucose(payload: PredictRequest):
    try:
        return twin_engine.predict_future_glucose(
            payload.patient_id,
            payload.recent_glucose,
            payload.current_steps,
            payload.current_sleep
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/scenario", response_model=ScenarioResponse)
def scenario_simulation(payload: ScenarioRequest):
    try:
        return twin_engine.simulate_counterfactual(
            payload.patient_id,
            payload.baseline_glucose,
            payload.delta_carbs_g,
            payload.delta_activity_minutes,
            payload.delta_sleep_hours
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/model/metrics")
def get_model_metrics():
    if METRICS_PATH.exists():
        with open(METRICS_PATH, "r") as f:
            return json.load(f)
    return twin_engine.metrics or {"note": "Model metrics not computed yet."}