from pydantic import BaseModel, Field
from typing import List, Optional

class PatientProfileSchema(BaseModel):
    patient_id: str
    age: int
    gender: str
    bmi: float
    hba1c: float
    diabetes_type: str
    baseline_insulin_sensitivity: float

class ObservationSchema(BaseModel):
    timestamp: str
    glucose_mg_dl: float
    steps: int
    sleep_hours: float
    carbs_consumed_g: Optional[float] = 0.0

class PredictRequest(BaseModel):
    patient_id: str
    recent_glucose: List[float] = Field(..., description="Last 5 glucose readings at 5-min intervals")
    current_steps: int = 0
    current_sleep: float = 7.0

class PredictResponse(BaseModel):
    patient_id: str
    predicted_glucose_30min: float
    horizon_minutes: int = 30
    model_version: str = "glucotwin-v1.0.0-rf"
    confidence_interval: List[float]
    data_quality_status: str

class ScenarioRequest(BaseModel):
    patient_id: str
    baseline_glucose: float
    delta_carbs_g: float = Field(..., description="Additional meal carbs in grams")
    delta_activity_minutes: float = Field(..., description="Additional exercise duration in minutes")
    delta_sleep_hours: float = Field(..., description="Sleep adjustment in hours")

class ScenarioResponse(BaseModel):
    patient_id: str
    baseline_forecast: float
    scenario_forecast: float
    glucose_difference: float
    explanation: str