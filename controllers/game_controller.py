from flask import Blueprint, request, jsonify
from services.game_service import create_game, make_move, get_game
from services.auth_service import decode_auth_token
import logging

logging.basicConfig(level=logging.DEBUG)

game_blueprint = Blueprint('game', __name__)

# Route to create a new game
@game_blueprint.route('/create', methods=['POST'])
def create():
    auth_header = request.headers.get('Authorization')
    auth_token = auth_header.split(" ")[1] if auth_header else None
    
    logging.debug(f"Extracted token: {auth_token}")
    
    user_id = decode_auth_token(auth_token)

    if not user_id or isinstance(user_id, str):
        logging.warning("Authentication failed during game creation")
        return jsonify({"error": "Authentication failed"}), 401
    
    game = create_game()
    
    logging.info("Game created successfully")    
    return jsonify(game.to_dict()), 201

# Route to make a move in an existing game
@game_blueprint.route('/move', methods=['POST'])
def move():
    auth_header = request.headers.get('Authorization')
    auth_token = auth_header.split(" ")[1] if auth_header else None
    logging.debug(f"Extracted token: {auth_token}")
    user_id = decode_auth_token(auth_token)

    if not user_id or isinstance(user_id, str):
        logging.warning("Authentication failed during game move")
        return jsonify({"error": "Authentication failed"}), 401
    
    game_id = request.json.get('game_id')
    player = request.json.get('player')
    x = request.json.get('x')
    y = request.json.get('y')
    
    game, error_message = make_move(game_id, player, x, y)
    
    if error_message:
        logging.warning(f"Move failed: {error_message}")
        return jsonify({"error": error_message}), 400
    
    logging.info("Move executed successfully")    
    return jsonify(game.to_dict()), 200

# Route to get the current status of a game
@game_blueprint.route('/status/<game_id>', methods=['GET'])
def game_status(game_id):
    auth_header = request.headers.get('Authorization')
    auth_token = auth_header.split(" ")[1] if auth_header else None
    logging.debug(f"Extracted token: {auth_token}")
    user_id = decode_auth_token(auth_token)

    if not user_id or isinstance(user_id, str):
        logging.warning("Authentication failed during game status check")
        return jsonify({"error": "Authentication failed"}), 401
    
    game = get_game(game_id)
    
    if not game:
        logging.warning("Game not found")
        return jsonify({"error": "Game not found"}), 404

    status = {
        "board": game.board,
        "player": game.current_player,
        "winner": game.winner
    }
    
    logging.info(f"Game status retrieved: {status}")    
    return jsonify(status)