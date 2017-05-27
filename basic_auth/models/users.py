from flask import current_app
from basic_auth import db
from sqlalchemy.exc import IntegrityError
import sqlalchemy
from datetime import datetime, timedelta

import hmac


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
    role_id = db.Column(db.Integer, db.ForeignKey("user_roles.role_id"), nullable=False)

    def view(self):
        view = {
            'user_id': self.user_id,
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at
        }
        return view

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True


def get_user(username):
    return UserModel.query.filter_by(username=username).first()


def get_user_by_id(user_id):
    return UserModel.query.filter_by(user_id=user_id).first()


def get_verified_users(verified=1, role_id=None):
    query = UserModel.query.filter_by(verified=verified)
    if role_id:
        query.filter_by(role_id=role_id)
    return query.all()


def delete_user_by_id(user_id):
    user = get_user_by_id(user_id)
    if user:
        user.delete()


def create_user(raw):
    try:
        add_user = UserModel()
        add_user.email = raw['email']
        add_user.username = raw['username']
        add_user.bcrypt_password = raw['password']
        add_user.verified = 1
        add_user.status = 1
        add_user.role_id = 1
        db.session.add(add_user)
        db.session.commit()

        return add_user.view()
    except IntegrityError:
        db.session.rollback()
        return None


class SessionModel(db.Model):
    """docstring for TokenJWT"""
    __tablename__ = 'user_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    session_id = db.Column(db.String(100), nullable=False)
    expired = db.Column(db.TIMESTAMP, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def view(self):
        return self.query.filter_by(user_id=self.user_id).first()

    @property
    def is_expired(self):
        if self.expired > datetime.now():
            return False
        return True


def get_session_by_user_id(user_id):
    return SessionModel.query.filter_by(user_id=user_id).first()


def get_session_by_id(session_id):
    return SessionModel.query.filter_by(session_id=session_id).first()


def generate_session(user_id):
    try:
        expired = datetime.now() + timedelta(days=30)
        session_id = generate_session_id(expired)
        add_session = SessionModel()
        add_session.user_id = user_id
        add_session.session_id = session_id
        add_session.expired = expired
        db.session.add(add_session)
        db.session.commit()
        return add_session.view()
    except IntegrityError:
        db.session.rollback()
        return None


def update_session(user_id):
    try:
        expired = datetime.now() + timedelta(days=30)
        session_id = generate_session_id(expired)
        session = get_session_by_user_id(user_id)
        session.session_id = session_id
        session.expired = expired
        session.save()
        return session.view()
    except IntegrityError:
        db.session.rollback()
        return None


def generate_session_id(expired):
    session_id = hmac.new(current_app.config.get('APP_SECRET'), expired.strftime('%Y-%m-%d %H:%m:%s'))
    return session_id.digest().encode("hex")


class UserRoleModel(db.Model):
    """docstring for UserRoleModel"""
    __tablename__ = 'user_roles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), nullable=False)
