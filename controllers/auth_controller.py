from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    user = register_user(username, password)
    return jsonify(user.to_dict()), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user, token = login_user(username, password)
    return jsonify({'user': user.to_dict(), 'token': token}), 200
