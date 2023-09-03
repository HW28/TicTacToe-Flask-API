# test_app.py

import pytest
import json
from app import app, db
from services.game_service import make_move
from models.user import User
from models.game import Game


# Define fixture to setup and teardown the test database
@pytest.fixture(scope='function')
def client():
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'

    # Initialize client and database
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            new_game = Game()
            db.session.add(new_game)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()


# Test registration and login functionalities
def test_register_and_login(client):
    data = {"username": "testuser", "password": "testpassword"}
    response = client.post('/register', json=data)
    assert response.status_code == 201
    response = client.post('/login', json=data)
    assert response.status_code == 200


# Test entire game flow
def test_game_flow(client):
    data = {"username": "testuser", "password": "testpassword"}
    response = client.post('/register', json=data)
    token_data = json.loads(client.post('/login', json=data).data)
    token = token_data['token']

    headers = {'Authorization': f'Bearer {token}'}

    # Star Game
    response = client.post('/create', headers=headers)
    assert response.status_code == 201
    game_data = json.loads(response.data)
    game_id = game_data['id']

    # Make a move
    data = {"game_id": game_id, "player": "X", "x": 0, "y": 0}
    response = client.post('/move', headers=headers, json=data)
    assert response.status_code == 200

    # Check game status
    response = client.get(f'/status/{game_id}', headers=headers)
    assert response.status_code == 200


# Test User model functions
def test_user_model(client):
    # Register new user, test endpoint /register
    data = {"username": "testuser_model", "password": "testpassword"}
    client.post('/register', json=data)

    # Search user in the database
    user = User.query.filter_by(username='testuser_model').first()

    # Check user created
    assert user is not None

    # Check user password
    assert user.check_password('testpassword')


# Test the make_move function from game_service
def test_make_move(client):
    # Setting up the application context so we can interact with
    # the database and app configurations
    with app.app_context():

        # Test making a valid move in the game
        game, error = make_move(1, 'X', 0, 0)
        assert game is not None
        assert error is None
        assert game.current_player == 'O'

        # Test making an invalid move with negative x coordinate
        game, error = make_move(1, 'X', -1, 0)
        assert game is None
        assert error == "Invalid coordinates"

        # Test making an invalid move outside the game grid
        game, error = make_move(1, 'O', 3, 3)
        assert game is None
        assert error == "Invalid coordinates"

        # Test making another invalid move with negative y coordinate
        game, error = make_move(1, 'O', 0, -1)
        assert game is None          
        assert error == "Invalid coordinates"

        # Test making a valid move as 'O'
        game, error = make_move(1, 'O', 1, 1)
        assert game is not None
        assert error is None
        assert game.current_player == 'X'
