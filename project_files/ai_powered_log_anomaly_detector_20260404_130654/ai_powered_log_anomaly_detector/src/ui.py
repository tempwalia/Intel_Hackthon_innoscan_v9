import streamlit as st
import requests
import time
from datetime import datetime

# Streamlit UI
st.set_page_config(page_title="Log Anomaly Detector", layout="wide")

st.title("AI-Powered Log Anomaly & Root Cause Detector")
st.markdown("Upload logs for real-time anomaly detection and root cause analysis")

# Initialize session state
if 'job_id' not in st.session_state:
    st.session_state.job_id = None
    st.session_state.status = "idle"
    st.session_state.results = None

# Upload logs
uploaded_file = st.file_uploader("Choose a CSV/JSON file", type=["csv", "json"])

if uploaded_file is not None:
    try:
        # Read file
        if uploaded_file.name.endswith(".csv"):
            logs = pd.read_csv(uploaded_file).to_dict(orient="records")
        else:
            logs = pd.read_json(uploaded_file).to_dict(orient="records")
        
        # Submit to backend
        response = requests.post("http://localhost:8000/upload_logs", json={"logs": logs})
        response.raise_for_status()
        
        st.session_state.job_id = response.json()["job_id"]
        st.session_state.status = "processing"
        st.session_state.results = None
        
        st.success(f"Logs queued for analysis (Job ID: {st.session_state.job_id})")
    
    except Exception as e:
        st.error(f"Error uploading logs: {str(e)}")

# Check job status
if st.session_state.status == "processing":
    with st.spinner("Analyzing logs..."):
        while True:
            try:
                status_response = requests.get(f"http://localhost:8000/status?job_id={st.session_state.job_id}")
                status_response.raise_for_status()
                
                if status_response.json()["status"] == "completed":
                    st.session_state.status = "completed"
                    st.session_state.results = requests.get(f"http://localhost:8000/get_results?job_id={st.session_state.job_id}").json()
                    break
                
                time.sleep(2)
            except Exception as e:
                st.warning("Checking job status...")
                time.sleep(2)

# Display results
if st.session_state.status == "completed" and st.session_state.results:
    st.subheader("Analysis Results")
    
    # Display anomalies
    st.markdown("### Detected Anomalies")
    for anomaly in st.session_state.results["anomalies"]:
        st.markdown(f"**{anomaly['timestamp']}** - *{anomaly['log_snippet']}* (Severity: {anomaly['severity']})")
    
    # Display root causes
    st.markdown("### Root Cause Suggestions")
    for cause in st.session_state.results["root_causes"]:
        st.markdown(f"**Priority {cause['priority']}** - *{cause['explanation']}* (Confidence: {cause['confidence']:.2f})")

# Footer
st.markdown("---")
st.markdown("Powered by AI-Powered Log Anomaly & Root Cause Detector")