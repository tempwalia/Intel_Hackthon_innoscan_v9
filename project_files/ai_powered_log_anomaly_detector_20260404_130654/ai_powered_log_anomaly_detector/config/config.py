import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./faiss_index")
MAX_LOGS_PER_REQUEST = 1000
MAX_RETRIES = 3
LOG_LEVEL = "INFO"

---