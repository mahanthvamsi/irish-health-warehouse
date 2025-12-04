import pandas as pd
import random
import hashlib
from datetime import datetime, timedelta
import os

os.makedirs("../data", exist_ok=True)

hospitals = [
    {"id": 1, "name": "St. James's Hospital", "county": "Dublin"},
    {"id": 2, "name": "Mater Misericordiae", "county": "Dublin"},
    {"id": 3, "name": "Cork University Hospital", "county": "Cork"},
    {"id": 4, "name": "University Hospital Galway", "county": "Galway"},
]

diagnoses = ["J45.909", "J20.9", "I21.9", "E11.9"]
start_date = datetime(2023, 1, 1)
date_list = [start_date + timedelta(days=i) for i in range(730)]
rows = []

print("Generating Synthetic Irish Hospital Data...")

for date in date_list:
    is_winter = date.month in [11, 12, 1, 2]
    base_admissions = 55 if is_winter else 35

    for hospital in hospitals:
        today_count = int(base_admissions * random.uniform(0.8, 1.2))
        for _ in range(today_count):
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
df.to_csv("../data/irish_hospital_admissions.csv", index=False)
print(f"Generated {len(df)} hospital records.")