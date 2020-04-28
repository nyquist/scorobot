from pathlib import Path
from dotenv import load_dotenv
import os
from utils.backend_SQLite import SQLiteDB

load_dotenv("./storage/config/.env")
backend_location = "./storage/games.db"
print(Path(backend_location).absolute())
backend = SQLiteDB(backend_location)
token = os.getenv('DISCORD_TOKEN')

