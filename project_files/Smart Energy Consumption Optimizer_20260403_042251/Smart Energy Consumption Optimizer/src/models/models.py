from pydantic import BaseModel
from datetime import datetime

class SensorData(BaseModel):
    sensor_id: str
    timestamp: datetime
    power_usage: float
    temperature: float

class ForecastRequest(BaseModel):
    start_time: datetime
    end_time: datetime

class AlertRequest(BaseModel):
    sensor_id: str
    timestamp: datetime
    power_usage: float

class RecommendationResponse(BaseModel):
    timestamp: datetime
    recommendation: str