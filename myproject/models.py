from myproject import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    # username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    # profile_pic = db.Column(db.String(64), default='/static/pics/default.jpg', nullable=False)
    myid = db.Column(db.String(48), unique=True, nullable=False)

    # post = db.relationship('Posts', backref='author', lazy='dynamic')
    # user_comments = db.relationship('comments', backref='user_comments', lazy='joined')
    # id_check = db.relationship('media', backref='media_content', uselist=False)
    blocked_users = db.relationship('BlockedUsers', foreign_keys='BlockedUsers.user_id', backref='blocked_users',
                                    lazy='select', uselist=True)

    def __init__(self, email, password, myid):
        self.email = email
        self.password = generate_password_hash(password)
        self.myid = myid

    def check_password(self, field):
        return check_password_hash(self.password, field)


class BlockedUsers(db.Model):
    __tablename__ = 'Blocked_Users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(48), db.ForeignKey('users.myid'), nullable=False)
    blocked_user = db.Column(db.String(48), db.ForeignKey('users.myid'), nullable=False)


class active_users(db.Model):
    __tablename__ = 'active_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(48), db.ForeignKey('users.myid'), nullable=False, index=True)
    request_sid = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, request_sid):
        self.user_id = user_id
        self.request_sid = request_sid


class authenticated_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(48), db.ForeignKey('users.myid'), nullable=False, index=True)
    token = db.Column(db.String(48), unique=True, index=True)
    last_time_checked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token
