from your_database import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board = db.Column(db.String(9), nullable=False, default="-" * 9)
    winner = db.Column(db.String(1), nullable=True)
    current_player = db.Column(db.String(1), nullable=True, default="X")

    def to_dict(self):
        return {
            'id': self.id,
            'board': self.board,
            'winner': self.winner,
            'current_player': self.current_player
        }
