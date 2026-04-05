import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

class DataProcessor:
    def __init__(self):
        self.raw_data = pd.DataFrame(columns=['timestamp', 'device_id', 'power', 'temperature'])
        self.model = self._initialize_model()
    
    def _initialize_model(self):
        """Initialize Prophet model with default parameters"""
        from prophet import Prophet
        return Prophet()
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate incoming sensor data against constraints"""
        try:
            # Validate timestamp format
            datetime.fromisoformat(data['timestamp'])
            
            # Validate device ID
            if not (1 <= len(data['device_id']) <= 10 and data['device_id'].isalnum()):
                return False
                
            # Validate power range
            if not (0 <= data['power'] <= 1000):
                return False
                
            # Validate temperature range
            if not (-20 <= data['temperature'] <= 50):
                return False
                
            return True
            
        except (ValueError, KeyError) as e:
            return False
    
    def ingest_data(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Ingest and store sensor data"""
        if not self.validate_data(data):
            raise ValueError("Invalid data format")
            
        # Convert to DataFrame row
        row = pd.DataFrame([{
            'timestamp': data['timestamp'],
            'device_id': data['device_id'],
            'power': data['power'],
            'temperature': data['temperature']
        }])
        
        # Update raw data
        self.raw_data = pd.concat([self.raw_data, row], ignore_index=True)
        
        # Train model with latest data
        self._train_model()
        
        return {"status": "success", "message": "Data ingested"}
    
    def _train_model(self):
        """Train Prophet model with historical data"""
        if len(self.raw_data) < 100:
            return  # Need at least 100 data points for training
        
        # Prepare training data
        train_data = self.raw_data[['timestamp', 'power']]
        train_data.columns = ['ds', 'y']
        
        # Fit model
        self.model.fit(train_data)
    
    def get_forecast(self, hours: int = 24) -> List[Dict[str, float]]:
        """Generate power consumption forecasts"""
        future = self.model.make_future_dataframe(periods=hours*3600, freq='H')
        forecast = self.model.predict(future)
        
        # Format forecast data
        forecast_data = forecast[['ds', 'yhat']].rename(columns={'ds': 'timestamp', 'yhat': 'predicted_power'})
        return forecast_data.to_dict('records')
    
    def get_recommendations(self) -> List[Dict[str, str]]:
        """Generate optimization recommendations"""
        recommendations = []
        
        # Check for anomalies in last hour
        recent_data = self.raw_data[self.raw_data['timestamp'] > datetime.now() - timedelta(hours=1)]
        
        for _, row in recent_data.iterrows():
            if row['power'] > self.ANOMALY_THRESHOLD:
                severity = "high"
                action = "Reduce HVAC power"
                recommendations.append({
                    "action": action,
                    "severity": severity,
                    "timestamp": row['timestamp']
                })
        
        return recommendations