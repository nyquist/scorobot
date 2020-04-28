from pathlib import Path
from dotenv import load_dotenv
import os
from utils.backend_SQLite import SQLiteDB

load_dotenv("./storage/config/.env")
backend_location = "./storage/games.db"
print("Using backend: ", Path(backend_location).absolute())
print("Using token: ", os.getenv('DISCORD_TOKEN'))
backend = SQLiteDB(backend_location)
TOKEN = os.getenv('DISCORD_TOKEN')

