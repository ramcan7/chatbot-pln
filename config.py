import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / ".env"

load_dotenv(dotenv_path)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NGROK_PORT = int(os.getenv("NGROK_PORT"))
NGROK_URL = os.getenv("NGROK_URL")
CHATBOT_KEY = os.getenv("CHATBOT_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")