import faiss
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from loguru import logger

class AnomalyDetector:
    def __init__(self, index_path):
        self.index_path = index_path
        self.index = self._load_index()
        self.scaler = StandardScaler()
        
    def _load_index(self):
        try:
            index = faiss.read_index(self.index_path)
            logger.info(f"Loaded FAISS index from {self.index_path}")
            return index
        except Exception as e:
            logger.error(f"Failed to load FAISS index: {str(e)}")
            raise
    
    def detect_anomalies(self, embeddings):
        """Detect anomalies using FAISS similarity search"""
        try:
            # Normalize embeddings
            normalized = self.scaler.fit_transform(embeddings)
            
            # Search for nearest neighbors
            distances, indices = self.index.search(normalized, 2)
            
            # Identify anomalies (distance > threshold)
            threshold = np.percentile(distances[:, 1], 95)
            anomalies = distances[:, 1] > threshold
            
            return anomalies
        except Exception as e:
            logger.error(f"Anomaly detection failed: {str(e)}")
            raise

---