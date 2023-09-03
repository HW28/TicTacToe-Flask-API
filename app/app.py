from flask import Flask
from controllers.auth_controller import auth_blueprint
from controllers.game_controller import game_blueprint
from your_database import db
import logging
import sys
from os import environ


SQLALCHEMY_DATABASE_URI = environ.get('DB_URL',
                                      'sqlite:///test_database.db')

# Configure logging settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    stream=sys.stderr
)

# Initialize Flask application
app = Flask(__name__)

# Configure SQLAlchemy settings for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with Flask app
db.init_app(app)

# Register blueprints for routes
app.register_blueprint(auth_blueprint)
app.register_blueprint(game_blueprint)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
