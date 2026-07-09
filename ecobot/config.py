import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Google Sheets
GSHEET_CREDENTIALS_FILE = "credentials.json"  # скачаешь из Google Cloud
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# Настройки бота
MORNING_TIME = "09:00"  # время утреннего опроса
EVENING_TIME = "20:00"  # время вечернего чека