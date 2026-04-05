from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
import uvicorn
from src.data_processor import DataProcessor
from src.models import EnergyModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Smart Energy Consumption Optimizer")

# Initialize components
data_processor = DataProcessor()
energy_model = EnergyModel()

class SensorData(BaseModel):
    timestamp: str
    device_id: str
    power: float
    temperature: float

@app.post("/ingest")
async def ingest_sensor_data(data: SensorData):
    """Ingest sensor data for processing"""
    try:
        response = data_processor.ingest_data(data.dict())
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/forecast")
async def get_forecast(hours: int = 24):
    """Get power consumption forecasts"""
    forecast = energy_model.predict(hours)
    return forecast

@app.get("/recommendations")
async def get_recommendations():
    """Get optimization recommendations"""
    recommendations = energy_model.predict(1)  # Get 1 hour forecast for recommendations
    return {"recommendations": recommendations["forecast"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)