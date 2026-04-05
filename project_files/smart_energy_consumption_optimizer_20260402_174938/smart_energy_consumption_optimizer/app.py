import streamlit as st
import os
from src.dashboard import main as dashboard_main

if __name__ == "__main__":
    os.environ["STREAMLIT_SERVER_PORT"] = "8501"
    dashboard_main()