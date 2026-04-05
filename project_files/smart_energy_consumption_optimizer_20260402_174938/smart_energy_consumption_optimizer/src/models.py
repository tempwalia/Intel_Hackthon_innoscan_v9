from typing import Dict, Any
from datetime import datetime, timedelta
import pandas as pd
from prophet import Prophet

class EnergyModel:
    def __init__(self):
        self.processor = DataProcessor()
        self.last_training_time = datetime.now()
        
    def train_model(self):
        """Train model with latest data"""
        self.processor._train_model()
        self.last_training_time = datetime.now()
    
    def predict(self, hours: int = 24) -> Dict[str, Any]:
        """Generate forecasts"""
        forecast = self.processor.get_forecast(hours)
        return {
            "forecast": forecast,
            "last_training_time": self.last_training_time.isoformat()
        }