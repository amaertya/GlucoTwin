import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.app.services.data_simulator import generate_synthetic_cohort

if __name__ == "__main__":
    print("Generating GlucoTwin synthetic cohort datasets...")
    generate_synthetic_cohort()
    print("Dataset generated successfully inside data/ directory.")