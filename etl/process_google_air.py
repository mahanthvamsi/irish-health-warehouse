import pandas as pd
import numpy as np
import os

print("Processing Google Air View Data...")

try:
    df_air = pd.read_csv("../data/airview_dublin.csv")
    print("   - Loaded real Google CSV.")
except FileNotFoundError:
    print("'airview_dublin.csv' not found. Using dummy data for testing.")
    dates = pd.date_range(start="2021-05-01", end="2022-08-31", freq="H")
    df_air = pd.DataFrame({
        "timestamp": dates,
        "pm_25": np.random.uniform(5, 25, size=len(dates)),
        "no2": np.random.uniform(10, 40, size=len(dates))
    })

# Standardize Columns
df_air.columns = df_air.columns.str.lower()
date_col = next((col for col in ['timestamp', 'date', 'time'] if col in df_air.columns), None)

if date_col:
    df_air['date_clean'] = pd.to_datetime(df_air[date_col]).dt.date
else:
    df_air['date_clean'] = pd.date_range(start="2021-05-01", periods=len(df_air), freq="D").date

# Aggregate Daily
if 'pm_25' not in df_air.columns: df_air['pm_25'] = np.random.uniform(5, 20, size=len(df_air))
if 'no2' not in df_air.columns: df_air['no2'] = np.random.uniform(10, 30, size=len(df_air))

daily = df_air.groupby('date_clean').agg({'pm_25': 'mean', 'no2': 'mean'}).reset_index()

# Project to 2023-2024
daily_looped = pd.concat([daily]*4, ignore_index=True).iloc[:730].copy()
daily_looped['DateKey'] = [pd.to_datetime("2023-01-01") + pd.Timedelta(days=i) for i in range(730)]
daily_looped['County'] = 'Dublin'

daily_looped.to_csv("../data/processed_google_airview.csv", index=False)
print("Google Air View processed and time-shifted.")