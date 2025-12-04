import pandas as pd
import os

os.makedirs("../processed", exist_ok=True)
print("Merging datasets...")

try:
    df_hosp = pd.read_csv("../data/irish_hospital_admissions.csv")
    df_air = pd.read_csv("../data/processed_google_airview.csv")
except FileNotFoundError:
    print("Run the other two scripts first!")
    exit()

df_hosp['AdmissionDate'] = pd.to_datetime(df_hosp['AdmissionDate'])
df_air['DateKey'] = pd.to_datetime(df_air['DateKey'])

merged = pd.merge(df_hosp, df_air, left_on=["AdmissionDate", "County"], right_on=["DateKey", "County"], how="left")

# Impute missing data for Cork/Galway
for col in ['pm_25', 'no2']:
    merged[col] = merged[col].ffill()
    daily_means = merged.groupby('AdmissionDate')[col].transform('mean')
    merged[col] = merged[col].fillna(daily_means * 0.7)

merged.rename(columns={'pm_25': 'PM25', 'no2': 'NO2'}, inplace=True)
merged.to_csv("../processed/merged_health_environment.csv", index=False)
print(f"Warehouse Ready: {len(merged)} rows created.")