import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests

st.title("Smart Energy Consumption Optimizer")

# Forecast section
st.header("Energy Consumption Forecast")
start_date = st.date_input("Start Date", datetime.now())
end_date = st.date_input("End Date", datetime.now() + timedelta(days=1))

if st.button("Get Forecast"):
    start_time = datetime.combine(start_date, datetime.min.time())
    end_time = datetime.combine(end_date, datetime.min.time())
    response = requests.get(f"http://localhost:8000/forecast?start_time={start_time}&end_time={end_time}")
    forecast = response.json()
    st.write(forecast)

# Anomaly alerts section
st.header("Anomaly Alerts")
sensor_id = st.text_input("Sensor ID")
timestamp = st.text_input("Timestamp")
power_usage = st.number_input("Power Usage", min_value=0.0, max_value=1000.0)

if st.button("Check Alert"):
    response = requests.post("http://localhost:8000/alert", json={"sensor_id": sensor_id, "timestamp": timestamp, "power_usage": power_usage})
    st.write(response.json())

# Recommendations section
st.header("Optimization Recommendations")
if st.button("Get Recommendations"):
    response = requests.get("http://localhost:8000/recommendations")
    recommendations = response.json()
    st.write(recommendations)