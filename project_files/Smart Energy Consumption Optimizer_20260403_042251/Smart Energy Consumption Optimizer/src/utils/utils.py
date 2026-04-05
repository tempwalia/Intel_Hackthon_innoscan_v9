import pandas as pd
from datetime import datetime

def process_data(data):
    df = pd.DataFrame([{
        'sensor_id': data.sensor_id,
        'timestamp': data.timestamp,
        'power_usage': data.power_usage,
        'temperature': data.temperature
    }])
    return df

def detect_anomalies(data):
    threshold = 95  # 95% of baseline
    if data.power_usage > threshold:
        return True
    return False