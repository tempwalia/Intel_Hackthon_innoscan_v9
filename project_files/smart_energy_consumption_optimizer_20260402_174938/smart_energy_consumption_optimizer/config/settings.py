import os

class Settings:
    MODEL_TRAINING_INTERVAL = int(os.getenv("MODEL_TRAINING_INTERVAL", 3600))
    ANOMALY_THRESHOLD = float(os.getenv("ANOMALY_THRESHOLD", 1000))
    FORECAST_HOURS = int(os.getenv("FORECAST_HOURS", 24))