import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from backend.app.settings import ARTIFACTS_DIR, METRICS_PATH, MODEL_PATH
from backend.app.services.data_simulator import load_cohort_data
import json

def train_model():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    df_patients, df_obs = load_cohort_data()
    
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
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    model = RandomForestRegressor(n_estimators=60, max_depth=12, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mae = float(mean_absolute_error(y_test, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    r2 = float(r2_score(y_test, y_pred))
    
    y_baseline = X_test["glucose_mg_dl"]
    base_mae = float(mean_absolute_error(y_test, y_baseline))
    
    metrics = {
        "model": "RandomForestRegressor",
        "horizon_minutes": 30,
        "mae": round(mae, 3),
        "rmse": round(rmse, 3),
        "r2_score": round(r2, 3),
        "persistence_baseline_mae": round(base_mae, 3),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "note": "Trained on GlucoTwin synthetic ambulatory cohort with chronological split."
    }
    
    joblib.dump(model, MODEL_PATH)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)
        
    print(f"GlucoTwin model trained. MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.2f}")

if __name__ == "__main__":
    train_model()