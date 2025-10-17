import os
from datetime import datetime
from pathlib import Path

WITH_DEBUG = os.getenv('DEBUG') == '1'

BASE_DIR = Path(__file__).resolve().parent.parent

# db
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = int(os.getenv('DATABASE_PORT'))
DATABASE_NAME = os.getenv('DATABASE_NAME')

# log
LOG_DIR = BASE_DIR / 'logs'
LOG_PATH = LOG_DIR / f'{datetime.now().strftime('%Y-%m-%d')}.log'

# todoism
TODOISM_ITEM_PER_PAGE = 20

# flask
SECRET_KEY = os.getenv('SECRET_KEY', 'YpL0hE3qZ8mT6vW2rK9cN1bF4sU7jX5')
