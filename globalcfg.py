from pathlib import Path
from dotenv import load_dotenv
import os
from utils.backend_SQLite import SQLiteDB

load_dotenv("./storage/config/.env")
backend_location = "./storage/games.db"
TESTING = os.getenv('SCOROBOT_MODE') == 'TESTING'
if TESTING:
    backend_location = "./storage/test.db"
print("Using backend: ", Path(backend_location).absolute())
print("Using token: ", os.getenv('DISCORD_TOKEN'))
backend = SQLiteDB(backend_location)
TOKEN = os.getenv('DISCORD_TOKEN')

