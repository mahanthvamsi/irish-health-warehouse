import pandas as pd
import random
import hashlib
from datetime import datetime, timedelta
import os

# Ensure output directory exists
os.makedirs("../data", exist_ok=True)

# 1. Configuration
hospitals = [
    {"id": 1, "name": "St. James's Hospital", "county": "Dublin"},
    {"id": 2, "name": "Mater Misericordiae", "county": "Dublin"},
    {"id": 3, "name": "Cork University Hospital", "county": "Cork"},
    {"id": 4, "name": "University Hospital Galway", "county": "Galway"},
]

diagnoses = [
    "J45.909", # Asthma
    "J20.9",   # Acute Bronchitis
    "I21.9",   # Cardiac Arrest (Pollution sensitive)
    "E11.9"    # Diabetes
]

# 2. Date Range (Matching the Project Timeline: 2023-2024)
start_date = datetime(2023, 1, 1)
num_days = 730 # 2 Years

date_list = [start_date + timedelta(days=i) for i in range(num_days)]
rows = []

print("Generating Synthetic Irish Hospital Data...")

for date in date_list:
    # Seasonality Logic: More sick people in Winter (Nov-Feb)
    is_winter = date.month in [11, 12, 1, 2]
    base_admissions = 55 if is_winter else 35

    for hospital in hospitals:
        # Add random daily variance
        today_count = int(base_admissions * random.uniform(0.8, 1.2))

        for _ in range(today_count):
            # Create Hashed Patient ID (GDPR Compliance)
            raw_id = f"{random.randint(1000000, 9999999)}W"
            hashed_id = hashlib.sha256(raw_id.encode()).hexdigest()

            rows.append({
                "AdmissionDate": date.strftime("%Y-%m-%d"),
                "HospitalID": hospital["id"],
                "HospitalName": hospital["name"],
                "County": hospital["county"],
                "DiagnosisCode": random.choice(diagnoses),
                "PatientHash": hashed_id,
                "LengthOfStay": random.randint(1, 14),
                "Age": random.randint(18, 95),
                "Gender": random.choice(["M", "F"])
            })

df = pd.DataFrame(rows)
output_path = "../data/irish_hospital_admissions.csv"
df.to_csv(output_path, index=False)
print(f"Success: Generated {len(df)} rows at {output_path}")