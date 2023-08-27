from models.game import Game
from your_database import db

def check_winner(board):
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != "-":
            return board[i]

    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != "-":
            return board[i]

    if board[0] == board[4] == board[8] != "-" or board[2] == board[4] == board[6] != "-":
        return board[4]

    if "-" not in board:
        return "draw"

    return None


def create_game():
    game = Game()
    db.session.add(game)
    db.session.commit()
    return game

def make_move(game_id, player, x, y):
    game = Game.query.get(game_id)

    if game is None:
        return None, "Game not found"
    if game.winner is not None:
        return None, "Game has already ended"
    if game.current_player != player:
        return None, "Not the current player's turn"

    index = x * 3 + y
    board = list(game.board)
    if board[index] != "-":
        return None, "Invalid move"

    board[index] = player
    game.board = "".join(board)
    winner = check_winner(game.board)

    if winner:
        game.winner = winner if winner != "draw" else None
        game.current_player = None
    else:
        game.current_player = "O" if player == "X" else "X"

    db.session.commit()
    return game, None

def get_game(game_id):
    return Game.query.get(game_id)