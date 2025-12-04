import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Irish Health Warehouse", layout="wide", page_icon="🇮🇪")

# --- AWS CONFIGURATION ---
AWS_BUCKET_URL = "https://irish-health-25201340.s3.eu-west-1.amazonaws.com/merged_health_environment.csv"

@st.cache_data
def load_data():
    try:
        # Load directly from AWS S3 (Data Lake)
        df = pd.read_csv(AWS_BUCKET_URL)
        df["AdmissionDate"] = pd.to_datetime(df["AdmissionDate"])
        return df
    except Exception as e:
        st.error(f"Could not connect to AWS S3: {e}")
        return None

df = load_data()
if df is None: st.stop()

# --- DASHBOARD LOGIC ---
st.sidebar.header("🔍 Filters")
hospital_list = df["HospitalName"].unique()
selected_hospital = st.sidebar.selectbox("Select Hospital", hospital_list)

filtered_df = df[df["HospitalName"] == selected_hospital].sort_values("AdmissionDate")

st.title("🇮🇪 Irish Health Warehouse (AWS Edition)")
st.caption(f"Data sourced from AWS S3 | Analysis Target: {selected_hospital}")
st.divider()

col1, col2, col3 = st.columns(3)
col1.metric("🏥 Total Admissions", f"{len(filtered_df):,}")
col2.metric("🌫️ Avg PM2.5", f"{filtered_df['PM25'].mean():.1f} µg/m³")
col3.metric("⚠️ Pollution Spikes", f"{len(filtered_df[filtered_df['PM25'] > 15])}")

st.subheader("📉 Correlation: Pollution vs. Admissions")
daily = filtered_df.groupby("AdmissionDate").agg({"HospitalID": "count", "PM25": "mean"}).rename(columns={"HospitalID": "Admissions"})

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(x=daily.index, y=daily['Admissions'], name="Admissions", marker_color='rgba(26, 118, 255, 0.5)'), secondary_y=False)
fig.add_trace(go.Scatter(x=daily.index, y=daily['PM25'], name="PM2.5 (Google Air View)", line=dict(color='red', width=2)), secondary_y=True)
st.plotly_chart(fig, use_container_width=True)