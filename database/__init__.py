from dotenv import load_dotenv
from pathlib import Path
import os

from database.connection import SQLiteDBConnection

dotenv_path = Path('config.env')
load_dotenv(dotenv_path=dotenv_path)
DB_FILE = os.getenv('custom_db_name')
db_instance = SQLiteDBConnection(db_file=DB_FILE)
