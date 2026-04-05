from fastapi import FastAPI
from uvicorn import run
from src.api import app as api_app

if __name__ == "__main__":
    run(api_app, host="0.0.0.0", port=8000)