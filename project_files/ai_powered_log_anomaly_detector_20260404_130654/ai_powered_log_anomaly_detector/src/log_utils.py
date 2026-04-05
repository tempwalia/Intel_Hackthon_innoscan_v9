import pandas as pd
from datetime import datetime
from pydantic import BaseModel, validator
from loguru import logger

class LogSchema(BaseModel):
    timestamp: str
    level: str
    message: str
    
    @validator('timestamp')
    def validate_timestamp(cls, value):
        try:
            datetime.fromisoformat(value)
            return value
        except ValueError:
            raise ValueError("Invalid ISO 8601 timestamp format")
    
    @validator('level')
    def validate_log_level(cls, value):
        if value not in ["ERROR", "WARN", "INFO", "DEBUG"]:
            raise ValueError("Invalid log level")
        return value

def process_logs(logs):
    """Process and validate log data"""
    try:
        # Validate and parse logs
        validated_logs = [LogSchema(**log) for log in logs]
        
        # Convert to DataFrame
        df = pd.DataFrame([log.dict() for log in validated_logs])
        
        # Normalize timestamps
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        return df
    except Exception as e:
        logger.error(f"Log processing failed: {str(e)}")
        raise

---