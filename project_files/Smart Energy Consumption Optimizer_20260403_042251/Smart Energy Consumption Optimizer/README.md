# Smart Energy Consumption Optimizer

## Setup Instructions

1. Clone the repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the FastAPI server:
   ```
   uvicorn src.main:app --reload
   ```
4. Run the Streamlit dashboard:
   ```
   streamlit run dashboard.py
   ```

## Features

- Ingest real-time IoT sensor data.
- Predict energy consumption using Prophet.
- Detect anomalies and generate optimization recommendations.
- Interactive dashboard for real-time visualization.

## Requirements

- Python 3.9+
- MQTT broker (e.g., Mosquitto)
- Cloud storage (e.g., AWS S3)