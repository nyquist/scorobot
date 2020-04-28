from utils.backend_SQLite import SQLiteDB
from pathlib import Path

backend_location = Path('.') / "storage" / "games.db"
backend = SQLiteDB(backend_location)