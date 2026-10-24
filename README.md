# GlucoTwin - Personalized Glucose Response Digital Twin

## Team Details
* **Team Name:** GlucoTwin Team
* **Developer / Lead:** Amartya BS

## College/Incubator Information
* Happiest Health Challenge 2026 Participant

## Project Title
**GlucoTwin: AI-Powered Personalised Glucose Response Digital Twin**

## Problem Statement
Managing diabetes and interpreting Continuous Glucose Monitoring (CGM) data requires proactive forecasting rather than passive tracking. Standard monitors display real-time glucose values but lack predictive trajectory modelling and interactive simulation capabilities to evaluate lifestyle decisions (such as meals and activity) before they occur.

## Healthcare Use Case
GlucoTwin establishes a physiological digital twin framework for individuals to support precision glucose management:
* **Short-Term Forecasting:** 15-minute and 30-minute CGM trajectory forecasting.
* **Longitudinal Patient Analysis:** Cohort tracking across key biomarkers like HbA1c and BMI.
* **Virtual Patient Simulation:** Risk stratification and scenario simulation in an interactive lab environment.

## Technical Stack
* **Backend:** Python 3.13, FastAPI, Uvicorn, Pandas, NumPy, Scikit-Learn
* **Frontend:** HTML5, CSS3, JavaScript (ES6), Chart.js
* **Data Processing & Pipelines:** Synthetic CGM data generation engine, twin training and evaluation scripts

## AI/ML Model or Framework Details
* **Data Synthesis (`backend/scripts/generate_synthetic_data.py`):** Generates realistic continuous glucose monitor streams along with baseline patient metrics.
* **Model Training (`backend/scripts/train_twin_model.py`):** Trains predictive digital twin models tuned on personalized baseline metrics.
* **Model Evaluation (`backend/scripts/evaluate_twin_model.py`):** Evaluates model predictive performance and mean absolute error (MARD).

## 15-20 Minute Demo Video Link
* **YouTube Video:** [https://youtu.be/eewgbVNBC0k]

## Open-Source License Details
This project is open-source software made available under the **MIT License**.

## Architecture Diagram & Presentation
* **Architecture Diagram:** Available in the project repository (`docs/architecture.pdf` / `docs/architecture.png`)
* **Presentation Deck:** Available in the project repository (`docs/presentation.pdf` / `docs/presentation.pptx`)
