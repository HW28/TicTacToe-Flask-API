from flask import Flask
from controllers.auth_controller import auth_blueprint
from controllers.game_controller import game_blueprint
from your_database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(game_blueprint)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)