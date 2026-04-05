import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import requests
from src.models import EnergyModel

# Initialize model
energy_model = EnergyModel()

# Streamlit app
st.set_page_config(page_title="Smart Energy Consumption Optimizer", layout="wide")

# Sidebar
st.sidebar.header("Energy Dashboard")
forecast_hours = st.sidebar.slider("Forecast Hours", min_value=1, max_value=24, value=24)

# Main content
st.title("Smart Energy Consumption Optimizer")
st.markdown("### Real-time Energy Monitoring and Optimization")

# Forecast chart
forecast = energy_model.predict(forecast_hours)
forecast_df = pd.DataFrame(forecast)
fig = px.line(forecast_df, x='timestamp', y='predicted_power', title='Power Consumption Forecast')
st.plotly_chart(fig, use_container_width=True)

# Anomaly alerts
st.markdown("### Anomaly Alerts")
alerts = energy_model.predict(1)  # Get 1 hour forecast for alerts
for alert in alerts["forecast"]:
    severity = "high" if alert["predicted_power"] > float(os.getenv("ANOMALY_THRESHOLD", 1000)) else "medium"
    st.markdown(f"⚠️ {severity} Alert: {alert['timestamp']} - {alert['predicted_power']}W")

# Recommendations
st.markdown("### Optimization Recommendations")
recommendations = energy_model.predict(1)
for rec in recommendations["forecast"]:
    st.markdown(f"💡 {rec['timestamp']} - {rec['predicted_power']}W: {rec['action']}")