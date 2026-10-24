import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
DATA_DIR = BASE_DIR / "data"

MODEL_PATH = ARTIFACTS_DIR / "glucotwin_random_forest.joblib"
METRICS_PATH = ARTIFACTS_DIR / "evaluation_metrics.json"
PATIENTS_DATA_PATH = DATA_DIR / "glucotwin_patients.csv"
OBSERVATIONS_DATA_PATH = DATA_DIR / "glucotwin_observations.csv"