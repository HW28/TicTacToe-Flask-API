from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from os import environ


SECRET_KEY = environ.get('SECRET_KEY', 'secret')

# Define the JWT expiration period (1 day in this case)
JWT_EXPIRATION_DELTA = timedelta(days=1)

# Initialize SQLAlchemy database object
db = SQLAlchemy()
