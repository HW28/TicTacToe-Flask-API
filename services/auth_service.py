from models.user import User
from your_database import db
import jwt
from your_database import SECRET_KEY
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError
import logging

logging.basicConfig(level=logging.DEBUG)

# Function to register a new user
def register_user(username, password):
    logging.info(f"Registering user with username: {username}")

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        logging.warning(f"User {username} already exists")
        return None
    user = User(username=username)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    logging.info(f"User registered successfully with username: {username}")    
    return user

# Function to login a user
def login_user(username, password):
    logging.debug(f"Attempt to log in with username: {username}")
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
        
        logging.info(f"User {username} logged in successfully")        
        return user, token

    logging.warning(f"Failed login attempt with username: {username}")    
    return None, None

# Function to decode JWT auth token
def decode_auth_token(auth_token):
    try:
        logging.debug("Attempting to decode auth token")
        
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        
        logging.debug(f"Token decoded successfully, payload: {payload}")        
        return payload['id']
    
    # Handle expired token signature
    except ExpiredSignatureError:
        logging.warning("Signature expired")
        raise InvalidTokenError("Signature expired. Please log in again.")
        
    # Handle invalid token
    except DecodeError:
        logging.warning("Invalid token")
        raise InvalidTokenError("Invalid token. Please log in again.")
        
    # Handle any other exceptions
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise InvalidTokenError("An error occurred. Please try again.")
