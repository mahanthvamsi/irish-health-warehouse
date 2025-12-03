import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Page Config
st.set_page_config(page_title="Irish Health Warehouse", layout="wide", page_icon="🇮🇪")

# 2. Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("../processed/merged_health_environment.csv")
        df["AdmissionDate"] = pd.to_datetime(df["AdmissionDate"])
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("Data not found! Please run the scripts in the 'etl' folder first.")
    st.stop()

# 3. Sidebar
st.sidebar.header("🔍 Filters")
hospital_list = df["HospitalName"].unique()
selected_hospital = st.sidebar.selectbox("Select Hospital", hospital_list)

filtered_df = df[df["HospitalName"] == selected_hospital].sort_values("AdmissionDate")

# Sidebar Metrics
avg_pm = filtered_df["PM25"].mean()
st.sidebar.markdown("### 🌫️ Google Air View Avg")
st.sidebar.metric("PM2.5 Level", f"{avg_pm:.1f} µg/m³")
st.sidebar.info("Data Source: Google Project Air View (Dublin) projected to 2023-24")

# 4. Main Title
st.title("🇮🇪 Irish Respiratory Health Warehouse")
st.markdown(f"**Analysis:** Impact of Air Quality on Admissions at *{selected_hospital}*")
st.divider()

# 5. KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("🏥 Total Admissions", f"{len(filtered_df):,}")
col2.metric("😷 Avg Daily Patients", f"{len(filtered_df)/730:.1f}")
high_pol_days = len(filtered_df[filtered_df['PM25'] > 15])
col3.metric("⚠️ High Pollution Days", f"{high_pol_days}")

# 6. Dual-Axis Chart
st.subheader("📉 Correlation: Pollution vs. Admissions")

# Aggregate to daily
daily = filtered_df.groupby("AdmissionDate").agg({
    "HospitalID": "count",
    "PM25": "mean"
}).rename(columns={"HospitalID": "Admissions"})

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Admissions (Bars)
fig.add_trace(
    go.Bar(x=daily.index, y=daily['Admissions'], name="Admissions", marker_color='rgba(26, 118, 255, 0.5)'),
    secondary_y=False
)

# Pollution (Line)
fig.add_trace(
    go.Scatter(x=daily.index, y=daily['PM25'], name="PM2.5 (Google Air View)", line=dict(color='red', width=2)),
    secondary_y=True
)

fig.update_layout(title_text="Do Admissions Spike when Pollution Rises?", height=500)
fig.update_yaxes(title_text="Admissions", secondary_y=False)
fig.update_yaxes(title_text="PM2.5 Level", secondary_y=True)

st.plotly_chart(fig, use_container_width=True)

# 7. Raw Data
with st.expander("🔎 View Source Data"):
    st.dataframe(filtered_df.head(100), use_container_width=True)