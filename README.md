# Irish Health Data Warehouse (AWS Cloud Project)

**COMP47780 - Cloud Computing Project**  
**Mahanth Vamsi Katragunta - 25201340**

---

## Overview

This project implements a fully **cloud-based healthcare data warehouse** using **Amazon Web Services (AWS)**. It integrates granular hospital admissions data with environmental pollution readings to analyze the impact of air quality on respiratory-related hospital visits across Ireland.

The solution includes:

- Custom Python-based ETL (Extract, Transform, Load) pipelines  
- A cloud data warehouse on **AWS S3**  
- An interactive dashboard deployed via **AWS EC2**  
- Visual analytics with **Streamlit** and **Plotly**

The final dashboard is publicly accessible, demonstrating an end-to-end solution for environmental health analytics.

---

##  Datasets

### Synthetic Irish Hospital Admissions (2023–2024)

**Features include:**
- Admission date  
- Diagnosis code  
- Age, gender  
- Length of stay  
- Hashed patient ID  

**Hospitals covered:**
- Dublin  
- Cork  
- Galway  

### Google Project Air View (Environmental Data)

- PM2.5 and NO₂ pollution readings  
- Hourly data aggregated into **daily averages**  
- Time-aligned with 2023–2024  

---

##  ETL Pipeline

###  [`generate_hospital_data.py`](https://github.com/mahanthvamsi/irish-health-warehouse/blob/main/etl/generate_hospital_data.py)
- Creates synthetic hospital admission data  
- Adds seasonal patterns  
- Hashes patient IDs  
- Generates diagnosis and LOS  

###  [`process_google_air.py`](https://github.com/mahanthvamsi/irish-health-warehouse/blob/main/etl/process_google_air.py)
- Cleans Google Air View dataset  
- Aggregates daily pollution averages  
- Time-shifts data to 2023–24  

###  [`etl_merge.py`](https://github.com/mahanthvamsi/irish-health-warehouse/blob/main/etl/etl_merge.py)
- Merges hospital + pollution datasets (date + county)  
- Handles missing values  
- Produces `merged_health_environment.csv`

**Final dataset is uploaded to AWS S3 (data warehouse).**

---

## System Architecture

![System Architecture](System_Architecture.png)

---

## Cloud Architecture (AWS)

- **AWS S3** → Stores final merged dataset  
- **AWS EC2** → Hosts Streamlit dashboard  
- **Ubuntu + Virtual Environment** → Python runtime  
- Dashboard publicly served on **port 8501**


---

## Dashboard Features

Built using **Streamlit** + **Plotly**, providing:

- Hospital selector  
- KPI metrics:  
  - Total admissions  
  - Average PM2.5  
  - Pollution spike count  
- Dual-axis visualizations (Admissions vs Pollution)  
- Raw dataset preview  
- Live data loading from AWS S3  

---

## Deploy on AWS EC2

### Launch EC2 Instance
- Choose **Ubuntu (20.04/22.04)** AMI  
- Select instance type (e.g., t2.micro)  
- Configure security group to allow:
  - **Port 22** — SSH  
  - **Port 8501** — Streamlit dashboard  

---

### Create and Activate a Virtual Environment
- python3 -m venv myenv 
- source myenv/bin/activate

### Install Dependencies
- pip install streamlit pandas plotly

### Run Streamlit App in Background
- nohup streamlit run app.py --server.address=0.0.0.0 --server.port=8501 &

---

## Dashboard URL
[http://108.130.86.13:8501/](http://108.130.86.13:8501/)
