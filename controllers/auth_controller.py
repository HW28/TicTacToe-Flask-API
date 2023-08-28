from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user
import logging

logging.basicConfig(level=logging.DEBUG)

auth_blueprint = Blueprint('auth', __name__)

# Route for user registration
@auth_blueprint.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    logging.info(f"Attempt to register with username: {username}")
    user = register_user(username, password)
    if user:
        logging.info(f"User {username} registered successfully")
        return jsonify(user.to_dict()), 201
    else:
        logging.warning(f"Failed to register user {username}")
        return jsonify({"error": "Registration failed"}), 400

# Route for user login
@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    logging.info(f"Attempt to log in with username: {username}")
    user, token = login_user(username, password)
    if user and token:
        logging.info(f"User {username} logged in successfully")
        return jsonify({'user': user.to_dict(), 'token': token}), 200
    logging.warning(f"Failed to log in user {username}")
    return jsonify({"error": "Login failed"}), 401