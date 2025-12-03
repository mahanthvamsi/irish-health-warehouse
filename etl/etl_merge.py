import pandas as pd
import os

os.makedirs("../processed", exist_ok=True)

print("Starting ETL Merge Process...")

# 1. Load the Generated/Processed Files
try:
    df_hosp = pd.read_csv("../data/irish_hospital_admissions.csv")
    df_air = pd.read_csv("../data/processed_google_airview.csv")
except FileNotFoundError:
    print("Critical Error: Run 'generate_hospital_data.py' and 'process_google_air.py' first.")
    exit()

# 2. Standardize Dates
df_hosp['AdmissionDate'] = pd.to_datetime(df_hosp['AdmissionDate'])
df_air['DateKey'] = pd.to_datetime(df_air['DateKey'])

# 3. Join Logic (Left Join)
# Hospital Data (Target) <--- Air Data (Source)
# Join Conditions: Date matches AND County matches
print("   - Merging datasets...")
merged_df = pd.merge(
    df_hosp,
    df_air,
    left_on=["AdmissionDate", "County"],
    right_on=["DateKey", "County"],
    how="left"
)

# 4. Handle Missing Data (Imputation)
# Since Google data is Dublin-only, Cork/Galway will be null.
# We fill them using Dublin trends but scaled down (cleaner air)
cols_to_fill = ['pm_25', 'no2']
for col in cols_to_fill:
    # Forward fill to patch small gaps
    merged_df[col] = merged_df[col].ffill()
    
    # If still null (e.g. Cork), fill with Dublin value * 0.7
    # Note: We do this by calculating a global mean per day and applying it
    daily_means = merged_df.groupby('AdmissionDate')[col].transform('mean')
    merged_df[col] = merged_df[col].fillna(daily_means * 0.7)

# 5. Final Rename for Dashboard
merged_df.rename(columns={
    'pm_25': 'PM25',
    'no2': 'NO2'
}, inplace=True)

# 6. Save Final Warehouse File
output_path = "../processed/merged_health_environment.csv"
merged_df.to_csv(output_path, index=False)

print(f"ETL Complete! Final Warehouse saved: {output_path}")
print(f"   - Total Rows: {len(merged_df)}")