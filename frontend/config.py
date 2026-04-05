"""
Configuration and path constants for InnoScan application
"""

import os
from pathlib import Path

# Get base directory
BASE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Directory paths
EXCEPTION_DIR = os.path.join(BASE_DIR, "exception_poc")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
KNOWLEDGE_BASE_PATH = os.path.join(PROJECT_ROOT, "knowledge_base", "poc_files")
MANAGERS_FILE = os.path.join(BASE_DIR, "managers.json")
EMPLOYEES_FILE = os.path.join(BASE_DIR, "employees.json")

# Create necessary directories
for directory in [EXCEPTION_DIR, UPLOADS_DIR, KNOWLEDGE_BASE_PATH]:
    os.makedirs(directory, exist_ok=True)

# Flask app configuration
SECRET_KEY = 'your-secret-key-change-this-in-production'
DEBUG = False
HOST = '127.0.0.1'
PORT = 5001

# Retriever configuration
RETRIEVER_CONFIG = {
    'index_name': 'innoscan',
    'knowledge_base_path': KNOWLEDGE_BASE_PATH,
    'score_threshold': 0.7,
    'top_k': 1
}

# Ingestion configuration
INGESTION_CONFIG = {
    'index_name': 'innoscan',
    'chunk_size': 500,
    'chunk_overlap': 20
}

# Default credentials
DEFAULT_MANAGERS = {
    "managers": [
        {"id": "ram123", "password": "password123", "name": "Ram Kumar"},
        {"id": "shyaam123", "password": "password123", "name": "Shyaam Kumar"},
        {"id": "admin", "password": "admin123", "name": "Admin"}
    ]
}

DEFAULT_EMPLOYEES = {
    "employees": [
        {"id": "emp001", "password": "password123", "name": "Employee One"},
        {"id": "emp002", "password": "password123", "name": "Employee Two"},
        {"id": "emp003", "password": "password123", "name": "Employee Three"}
    ]
}
