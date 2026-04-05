# Software Requirements Specification (SRS)  
# AI‑Powered Log Anomaly & Root Cause Detector  

## 1. PROJECT OVERVIEW  
- **Title**: AI-Powered Log Anomaly & Root Cause Detector  
- **Description**: Automatically detect anomalies in application logs and suggest probable root causes.  
- **Problem Statement**: Teams manually scan massive log files during incidents, causing delayed resolution.  
- **Expected Outcome**: Faster incident detection with AI-generated anomaly insights and root-cause hints.  
- **Programming Language**: Python  
- **Approach**: Ingest logs → generate embeddings → detect anomalies using ML → summarize patterns using LLM.  
- **Technology Stack**: Python, OpenAI/Azure OpenAI, FAISS, Pandas, Streamlit  
- **Project Complexity**: Medium  

## 2. FUNCTIONAL REQUIREMENTS  
### Input/Processing  
- Accept log files in JSON or CSV format with timestamp, log level, and message fields.  
- Preprocess logs by normalizing timestamps and extracting key patterns.  

### Core Engine  
- **Anomaly Detection**: Use ML model to identify outliers in log embeddings (via FAISS).  
- **Root Cause Suggestion**: LLM (OpenAI GPT-3.5) generates root-cause hypotheses based on anomaly patterns.  

### API Endpoints  
- `POST /upload_logs`: Submit log data for analysis.  
- `GET /get_results`: Retrieve anomaly summary and root-cause suggestions.  
- `GET /status`: Check job progress (job ID required).  

### Output Format  
- JSON response with:  
  - `anomalies`: List of detected anomalies (timestamp, log snippet, severity).  
  - `root_causes`: LLM-generated hypotheses (priority, confidence, explanation).  

## 3. NON-FUNCTIONAL REQUIREMENTS  
### Performance  
- <500ms response time for log uploads.  
- 99.9% uptime during peak loads.  
- Process 1000 logs/second for anomaly detection.  

### Reliability  
- Auto-retry failed ML inference requests (max 3 retries).  
- Graceful degradation for missing log fields.  

### Scalability  
- Handle 10,000 logs/second with horizontal scaling.  
- Support distributed FAISS index for large datasets.  

## 4. TECHNICAL ARCHITECTURE  
### Stack  
- **Backend**: Python (FastAPI), OpenAI API, FAISS, Pandas.  
- **Frontend**: Streamlit for interactive UI.  
- **LLM**: OpenAI GPT-3.5 for root-cause summarization.  

### Components  
- **Log Ingestion**: CSV/JSON parser with schema validation.  
- **Embedding Generator**: Text-to-vector conversion using OpenAI embeddings.  
- **Anomaly Engine**: FAISS-based similarity search for outlier detection.  
- **LLM Interface**: REST API wrapper for OpenAI’s GPT-3.5.  
- **UI**: Streamlit dashboard for real-time results visualization.  

### Model/Framework Details  
- **ML Model**: Custom trained on 10k+ log samples (accuracy ≥ 90%).  
- **LLM Prompt**: Structured template for root-cause inference (e.g., "Explain likely causes for this log pattern").  

## 5. API SPECIFICATION  
### Request/Response Examples  
#### Upload Logs  
**Request**:  
```json
{
  "logs": [
    {"timestamp": "2023-10-01T12:00:00Z", "level": "ERROR", "message": "Database connection timeout"},
    {"timestamp": "2023-10-01T12:01:00Z", "level": "WARN", "message": "High CPU usage"}
  ]
}
```  
**Response**:  
```json
{
  "job_id": "log_12345",
  "status": "processing",
  "message": "Logs queued for analysis"
}
```  

#### Get Results  
**Request**:  
```json
{
  "job_id": "log_12345"
}
```  
**Response**:  
```json
{
  "job_id": "log_12345",
  "status": "completed",
  "anomalies": [
    {
      "timestamp": "2023-10-01T12:00:00Z",
      "log_snippet": "Database connection timeout",
      "severity": "HIGH"
    }
  ],
  "root_causes": [
    {
      "priority": 1,
      "confidence": 0.85,
      "explanation": "Potential database server downtime or network latency."
    }
  ]
}
```  

## 6. DATA & CATEGORIES  
### Predefined Classifications  
- **Log Levels**: ERROR, WARN, INFO, DEBUG.  
- **Anomaly Severity**: LOW, MEDIUM, HIGH.  
- **Root Cause Categories**: Network, Database, Application, Infrastructure.  

### Data Types  
- **Log Entries**: JSON/CSV with `timestamp`, `level`, `message`.  
- **Embeddings**: 768-dimensional vectors (OpenAI text-embedding-ada-002).  
- **Metadata**: Job ID, timestamp, user ID (for audit logs).  

## 7. INPUT CONSTRAINTS  
- **Field Limits**:  
  - Max 1000 logs per request.  
  - Timestamp must be ISO 8601 format.  
- **Format Rules**:  
  - Log messages must be ≤ 512 characters.  
  - Log level must be one of: ERROR, WARN, INFO, DEBUG.  

## 8. ERROR HANDLING  
| Status Code | Description               | Action                          |  
|-------------|---------------------------|---------------------------------|  
| 400         | Invalid log format        | Return error with schema details|  
| 429         | Rate limit exceeded       | Retry after 10 seconds          |  
| 500         | Internal server error     | Log error, retry with fallback  |  
| 404         | Job ID not found          | Return "Job not found" message  |  

## 9. ACCEPTANCE CRITERIA  
- **Anomaly Detection**: Detect anomalies in 500+ logs with ≥ 85% accuracy.  
- **Root Cause Suggestions**: Generate ≥ 3 hypotheses per anomaly.  
- **Error Handling**: All error codes and messages must match the table above.  
- **UI Responsiveness**: Streamlit dashboard loads in <2 seconds.  

## 10. DEPENDENCIES  
- **Python**: 3.9.12  
- **Packages**:  
  - `pandas` (1.5.3)  
  - `faiss-cpu` (1.7.3)  
  - `openai` (0.28.1)  
  - `streamlit` (1.26.0)  
  - `fastapi` (0.95.0)  
  - `uvicorn` (0.21.1)  

## 11. FUTURE ENHANCEMENTS  
- **Real-time Detection**: Stream logs from Kafka/CloudWatch.  
- **Model Optimization**: Use quantized FAISS for faster inference.  
- **Monitoring Integration**: Alert via Slack/Email on critical anomalies.  
- **User Feedback Loop**: Allow users to refine root-cause suggestions.