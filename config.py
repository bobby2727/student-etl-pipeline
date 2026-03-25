import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
DB_PATH = os.getenv("DB_PATH")
CSV_PATH = os.getenv("CSV_PATH")
LOG_FILE = os.getenv("LOG_FILE")