# Smart Energy Consumption Optimizer

## Getting Started

### Prerequisites
- Python 3.9.12
- Docker (optional for production deployment)

### Installation
1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
# Start backend
uvicorn main:app --reload

# Start frontend
streamlit run app.py
```

### API Documentation
Swagger UI available at http://localhost:8000/docs

## Features
- Real-time energy consumption forecasting
- Anomaly detection with threshold alerts
- Optimization recommendations
- Interactive dashboard with visualizations

## Configuration
Edit `.env` file to configure:
- MODEL_TRAINING_INTERVAL (default: 3600 seconds)
- ANOMALY_THRESHOLD (default: 1000W)