import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json
from backend.app.settings import MODEL_PATH, METRICS_PATH, ARTIFACTS_DIR
from backend.app.services.data_simulator import load_cohort_data

def evaluate_model():
    print("Loading GlucoTwin dataset and trained model artifacts...")
    df_patients, df_obs = load_cohort_data()
    
    if not MODEL_PATH.exists():
        print(f"Error: Model file not found at {MODEL_PATH}. Please run train_twin_model.py first.")
        return

    model = joblib.load(MODEL_PATH)
    
    df = df_obs.merge(df_patients, on="patient_id", how="left")
    
    df["glucose_lag1"] = df.groupby("patient_id")["glucose_mg_dl"].shift(1)
    df["glucose_lag2"] = df.groupby("patient_id")["glucose_mg_dl"].shift(2)
    df["glucose_lag3"] = df.groupby("patient_id")["glucose_mg_dl"].shift(3)
    df["target_glucose"] = df.groupby("patient_id")["glucose_mg_dl"].shift(-2)
    
    df = df.dropna()
    
    features = ["glucose_mg_dl", "glucose_lag1", "glucose_lag2", "glucose_lag3", "steps", "sleep_hours", "carbs_consumed_g", "age", "bmi", "hba1c"]
    X = df[features]
    y = df["target_glucose"]
    
    split_idx = int(len(X) * 0.8)
    X_test = X.iloc[split_idx:]
    y_test = y.iloc[split_idx:]
    
    y_pred = model.predict(X_test)
    mae = float(mean_absolute_error(y_test, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    r2 = float(r2_score(y_test, y_pred))
    
    y_baseline = X_test["glucose_mg_dl"]
    base_mae = float(mean_absolute_error(y_test, y_baseline))
    
    print("\n==========================================")
    print("       GLUCOTWIN EVALUATION RESULTS       ")
    print("==========================================")
    print(f"Test Samples evaluated: {len(X_test)}")
    print(f"Mean Absolute Error (MAE): {mae:.3f} mg/dL")
    print(f"Root Mean Squared Error (RMSE): {rmse:.3f} mg/dL")
    print(f"R² Score: {r2:.3f}")
    print(f"Persistence Baseline MAE: {base_mae:.3f} mg/dL")
    print("==========================================\n")
    
    metrics = {
        "model": "RandomForestRegressor",
        "horizon_minutes": 30,
        "mae": round(mae, 3),
        "rmse": round(rmse, 3),
        "r2_score": round(r2, 3),
        "persistence_baseline_mae": round(base_mae, 3),
        "test_samples": len(X_test),
        "note": "Independent evaluation run on GlucoTwin chronological test split."
    }
    
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)
        
    print(f"Evaluation metrics successfully saved to {METRICS_PATH}")

if __name__ == "__main__":
    evaluate_model()