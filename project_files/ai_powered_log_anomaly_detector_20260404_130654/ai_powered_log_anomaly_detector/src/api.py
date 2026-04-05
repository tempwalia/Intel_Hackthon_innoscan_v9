from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
from uuid import uuid4
import time
from loguru import logger
from .anomaly_engine import AnomalyDetector
from .llm_utils import LLMInterface
from .log_utils import process_logs

app = FastAPI()
anomaly_detector = AnomalyDetector("faiss_index")
llm_interface = LLMInterface()

# In-memory job tracking
jobs = {}

class LogUploadRequest(BaseModel):
    logs: List[Dict[str, str]]

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    message: str

class AnomalyResult(BaseModel):
    timestamp: str
    log_snippet: str
    severity: str

class RootCause(BaseModel):
    priority: int
    confidence: float
    explanation: str

class ResultsResponse(BaseModel):
    job_id: str
    status: str
    anomalies: List[AnomalyResult]
    root_causes: List[RootCause]

@app.post("/upload_logs")
async def upload_logs(request: LogUploadRequest):
    """Upload logs for analysis"""
    if len(request.logs) > 1000:
        raise HTTPException(status_code=400, detail="Max 1000 logs per request")
    
    try:
        # Process logs
        df = process_logs(request.logs)
        
        # Generate embeddings (simulated)
        embeddings = np.random.rand(len(df), 768)  # Simulated embeddings
        
        # Detect anomalies
        anomalies = anomaly_detector.detect_anomalies(embeddings)
        
        # Generate root causes
        root_causes = []
        for i, log in df.iterrows():
            if anomalies[i]:
                root_causes.extend(llm_interface.generate_root_causes(log['message']))
        
        # Store job results
        job_id = str(uuid4())
        jobs[job_id] = {
            "status": "completed",
            "anomalies": [{"timestamp": log['timestamp'], "log_snippet": log['message'], "severity": "HIGH"} for i, log in df.iterrows() if anomalies[i]],
            "root_causes": root_causes[:3]  # Limit to 3 top hypotheses
        }
        
        return JobStatusResponse(job_id=job_id, status="completed", message="Analysis completed")
    
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/get_results")
async def get_results(job_id: str):
    """Retrieve analysis results"""
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return ResultsResponse(**job)

@app.get("/status")
async def get_status(job_id: str):
    """Check job status"""
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatusResponse(job_id=job_id, status=job["status"], message="")

---