import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
WEB_DRIVER_HOST = os.getenv('WEB_DRIVER_HOST')
WEB_DRIVER_PORT = os.getenv('WEB_DRIVER_PORT')
