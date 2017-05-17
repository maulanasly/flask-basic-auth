from basic_auth import db
import sqlalchemy


class UserModel(db.Model):
    """docstring for UsersModel"""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    bcrypt_password = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=sqlalchemy.func.current_timestamp())
    verified = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=0)


def get_user(username):
    return UserModel.query.filter_by(username=username).first()


class SessionModel(db.Model):
    """docstring for TokenJWT"""
    __tablename__ = 'user_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    session_id = db.Column(db.String(100), nullable=False)
    expired = db.Column(db.TIMESTAMP, nullable=True)


def get_session_by_id(user_id):
    return SessionModel.query.filter_by(user_id=user_id).first()
