# AI-Powered Log Anomaly & Root Cause Detector

## Getting Started

### Prerequisites
- Python 3.9.12
- Docker (optional for production deployment)

### Setup
1. Clone repository:
```bash
git clone https://github.com/yourusername/ai_powered_log_anomaly_detector.git
cd ai_powered_log_anomaly_detector
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export OPENAI_API_KEY='your-openai-key'
export FAISS_INDEX_PATH='./faiss_index'
```

### Running the Application
```bash
# Start backend
uvicorn src.api:app --reload

# Start frontend
streamlit run src/ui.py
```

## Architecture Overview
- **Backend**: FastAPI with OpenAI/FAISS integration
- **Frontend**: Streamlit dashboard
- **Storage**: In-memory job tracking with FAISS index

## API Endpoints
- POST /upload_logs
- GET /get_results
- GET /status

## Error Codes
- 400: Invalid log format
- 429: Rate limit exceeded
- 500: Internal server error
- 404: Job ID not found

---