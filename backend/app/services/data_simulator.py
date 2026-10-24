import pandas as pd
import numpy as np
from backend.app.settings import DATA_DIR, PATIENTS_DATA_PATH, OBSERVATIONS_DATA_PATH

def generate_synthetic_cohort(num_patients: int = 10, days: int = 7):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    
    patients = []
    observations = []
    start_date = pd.Timestamp("2026-10-01 00:00:00")
    
    for i in range(1, num_patients + 1):
        pid = f"GT-PATIENT-{i:03d}"
        age = int(np.random.randint(42, 69))
        bmi = round(float(np.random.uniform(26.5, 39.0)), 1)
        hba1c = round(float(np.random.uniform(7.2, 9.9)), 1)
        
        patients.append({
            "patient_id": pid,
            "age": age,
            "gender": np.random.choice(["Male", "Female"]),
            "bmi": bmi,
            "hba1c": hba1c,
            "diabetes_type": "Type 2",
            "baseline_insulin_sensitivity": round(float(np.random.uniform(1.1, 2.4)), 2)
        })
        
        total_steps = days * 24 * 4
        current_time = start_date
        base_g = float(np.random.uniform(135, 185))
        
        for step in range(total_steps):
            noise = np.random.normal(0, 4.0)
            hour = current_time.hour
            meal_bump = 28.0 if hour in [13, 20] and step % 4 == 0 else 0.0
            
            base_g = 0.84 * base_g + 0.16 * (142 + meal_bump + noise)
            base_g = np.clip(base_g, 70.0, 330.0)
            
            steps_val = int(np.random.poisson(35) if 7 <= hour <= 21 else 2)
            sleep_val = 7.5 if hour < 6 or hour > 22 else 0.0
            carbs = 50.0 if meal_bump > 0 else 0.0
            
            observations.append({
                "patient_id": pid,
                "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "glucose_mg_dl": round(base_g, 1),
                "steps": steps_val,
                "sleep_hours": sleep_val,
                "carbs_consumed_g": carbs
            })
            current_time += pd.Timedelta(minutes=15)
            
    df_patients = pd.DataFrame(patients)
    df_obs = pd.DataFrame(observations)
    
    df_patients.to_csv(PATIENTS_DATA_PATH, index=False)
    df_obs.to_csv(OBSERVATIONS_DATA_PATH, index=False)
    return df_patients, df_obs

def load_cohort_data():
    if not PATIENTS_DATA_PATH.exists() or not OBSERVATIONS_DATA_PATH.exists():
        return generate_synthetic_cohort()
    return pd.read_csv(PATIENTS_DATA_PATH), pd.read_csv(OBSERVATIONS_DATA_PATH)