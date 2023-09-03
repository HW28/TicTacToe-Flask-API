from models.game import Game
from your_database import db
import logging

logging.basicConfig(level=logging.DEBUG)


# Function to check if there's a winner on the board
def check_winner(board):
    logging.debug(f"Checking winner, current board: {board}")

    # Check rows for a winner
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != "-":
            logging.info(f"Winner found in row: {board[i]}")
            return board[i]

    # Check columns for a winner
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != "-":
            logging.info(f"Winner found in column: {board[i]}")
            return board[i]

    # Check diagonals for a winner
    if (board[0] == board[4] == board[8] != "-" or
            board[2] == board[4] == board[6] != "-"):
        logging.info(f"Winner found in diagonal: {board[4]}")
        return board[4]

    # Check if the game is a draw
    if "-" not in board:
        logging.info("Draw detected")
        return "draw"

    logging.debug("No winner yet")
    return None


# Function to create a new game
def create_game():
    logging.info("Creating new game")
    game = Game()
    db.session.add(game)
    db.session.commit()
    logging.info(f"Game created with ID: {game.id}")
    return game


# Function to make a move in the game
def make_move(game_id, player, x, y):
    logging.debug(f"Move attempt by player {player} at position ({x}, {y}) "
                  f"for game with ID {game_id}")

    # Validate coordinates
    if not (0 <= x < 3) or not (0 <= y < 3):
        logging.warning("Invalid coordinates")
        return None, "Invalid coordinates"

    # Validate player ('X' or 'O')
    if player not in ["X", "O"]:
        logging.warning("Invalid player")
        return None, "Invalid player"

    game = db.session.get(Game, game_id)
    # Check if game exists
    if game is None:
        logging.warning(f"Game with ID {game_id} not found")
        return None, "Game not found"

    # Check if game has already ended
    if game.winner is not None:
        logging.info(f"The game with ID {game_id} has already ended")
        return None, "Game has already ended"

    # Check if it's the current player's turn
    if game.current_player != player:
        logging.warning("Not the current player's turn")
        return None, "Not the current player's turn"

    # Calculate board index and make the move
    index = x * 3 + y
    board = list(game.board)
    if board[index] != "-":
        logging.warning("Invalid move, cell already occupied")
        return None, "Invalid move"

    # Update board and check for a winner
    board[index] = player
    game.board = "".join(board)
    winner = check_winner(game.board)

    # Update game state based on move
    if winner:
        game.winner = winner if winner != "draw" else None
        game.current_player = None
    else:
        game.current_player = "O" if player == "X" else "X"

    db.session.commit()
    logging.info(f"Board updated: {game.board}, "
                 f"Player's turn: {game.current_player}")
    return game, None


# Function to get the current state of a game
def get_game(game_id):
    logging.debug(f"Retrieving game details with ID {game_id}")
    return db.session.get(Game, game_id)
