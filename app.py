import os

from todoism import create_app

config_name = os.getenv('DEBUG', 'development')

app = create_app()
