from fastapi import APIRouter, Depends, HTTPException
from src.models import SensorData, ForecastRequest, AlertRequest
from src.utils import process_data, detect_anomalies
from src.services import train_model, predict_forecast
from datetime import datetime
import pandas as pd

router = APIRouter()

@router.post("/ingest")
async def ingest_data(data: SensorData):
    if len(data.sensor_id) > 20:
        raise HTTPException(status_code=400, detail="sensor_id exceeds 20 characters")
    if data.power_usage < 0 or data.power_usage > 1000:
        raise HTTPException(status_code=400, detail="power_usage out of range")
    
    processed_data = process_data(data)
    return {"status": "success", "message": "Data ingested", "timestamp": data.timestamp}

@router.get("/forecast")
async def get_forecast(request: ForecastRequest):
    forecast = predict_forecast(request.start_time, request.end_time)
    return {"forecast": forecast}

@router.post("/alert")
async def trigger_alert(alert: AlertRequest):
    anomaly = detect_anomalies(alert)
    if anomaly:
        return {"status": "alert", "message": "Anomaly detected", "timestamp": alert.timestamp}
    return {"status": "success", "message": "No anomaly detected"}

@router.get("/recommendations")
async def get_recommendations():
    recommendations = generate_recommendations()
    return {"recommendations": recommendations}