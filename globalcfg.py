from pathlib import Path
from dotenv import load_dotenv
import os
from utils.backend_SQLite import SQLiteDB

load_dotenv("config/.env")
token = os.getenv('DISCORD_TOKEN')
DB_BASE = os.getenv('SCOROBOT_STORAGE_BASE')

backend_location = Path(DB_BASE) / "storage" / "games.db"
backend = SQLiteDB(backend_location)