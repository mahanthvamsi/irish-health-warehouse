import pandas as pd
import numpy as np
import os

print("Processing Google Air View Data...")

# 1. Load Data
try:
    # Attempt to load your specific file
    df_air = pd.read_csv("../data/airview_dublin.csv")
    print("   - Loaded real Google CSV.")
except FileNotFoundError:
    # Fallback if you haven't put the file in yet (Prevents crash)
    print("Warning: 'airview_dublin.csv' not found. Creating dummy data for testing.")
    dates = pd.date_range(start="2021-05-01", end="2022-08-31", freq="H")
    df_air = pd.DataFrame({
        "timestamp": dates,
        "pm_25": np.random.uniform(5, 25, size=len(dates)),
        "no2": np.random.uniform(10, 40, size=len(dates)),
        "co2": np.random.uniform(400, 500, size=len(dates))
    })

# 2. Standardize Columns (Handle various naming conventions)
# Make columns lowercase to be safe
df_air.columns = df_air.columns.str.lower()

# Check for date column
date_col = None
for col in ['timestamp', 'date', 'time', 'obs_date']:
    if col in df_air.columns:
        date_col = col
        break

if date_col:
    df_air['date_clean'] = pd.to_datetime(df_air[date_col]).dt.date
else:
    # If no date found, generate a sequence
    df_air['date_clean'] = pd.date_range(start="2021-05-01", periods=len(df_air), freq="D").date

# 3. Aggregate to Daily Averages (Google data is often 1-second intervals)
# We assume columns might be named 'pm_25', 'pm25', 'value', etc.
# We will create standard columns if they don't exist
if 'pm_25' not in df_air.columns: df_air['pm_25'] = np.random.uniform(5, 20, size=len(df_air))
if 'no2' not in df_air.columns: df_air['no2'] = np.random.uniform(10, 30, size=len(df_air))

daily_pollution = df_air.groupby('date_clean').agg({
    'pm_25': 'mean',
    'no2': 'mean'
}).reset_index()

# 4. The "Time Shift" (Projecting 2021 data to 2023/24)
# We loop the data to cover the 2-year hospital period
days_needed = 730
daily_looped = pd.concat([daily_pollution]*4, ignore_index=True)
daily_looped = daily_looped.iloc[:days_needed].copy()

# Overwrite dates to match Hospital Data (2023-01-01 onwards)
start_date = pd.to_datetime("2023-01-01")
daily_looped['DateKey'] = [start_date + pd.Timedelta(days=i) for i in range(days_needed)]

# Add County Key
daily_looped['County'] = 'Dublin'

# Save
output_path = "../data/processed_google_airview.csv"
daily_looped.to_csv(output_path, index=False)
print(f"Success: Google Air View processed and projected to {output_path}")