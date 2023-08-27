from models.user import User
from your_database import db
import jwt

def register_user(username, password):
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = jwt.encode({'id': user.id}, 'secret', algorithm='HS256')
        return user, token
    return None, None
