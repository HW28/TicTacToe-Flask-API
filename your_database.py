from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

# Define the JWT expiration period (1 day in this case)
JWT_EXPIRATION_DELTA = timedelta(days=1)

# Initialize SQLAlchemy database object
db = SQLAlchemy()