from flask import Blueprint, request, jsonify
from services.game_service import create_game, make_move, get_game

game_blueprint = Blueprint('game', __name__)

@game_blueprint.route('/create', methods=['POST'])
def create():
    game = create_game()
    return jsonify(game.to_dict()), 201

@game_blueprint.route('/move', methods=['POST'])
def move():
    game_id = request.json.get('game_id')
    player = request.json.get('player')
    x = request.json.get('x')
    y = request.json.get('y')
    game, error_message = make_move(game_id, player, x, y)
    if error_message:
        return jsonify({"error": error_message}), 400

    return jsonify(game.to_dict()), 200


@game_blueprint.route('/status/<game_id>', methods=['GET'])
def game_status(game_id):
    game = get_game(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    status = {
        "board": game.board,
        "player":game.current_player,
        "winner": game.winner
    }

    return jsonify(status)