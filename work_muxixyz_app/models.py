import time
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique = True)
    email = db.Column(db.String(35), unique = True)
    avatar = db.Column(db.String(50))
    tel = db.Column(db.String(15))
    role = db.Column(db.Integer)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    status = db.relationship('Statu', backref='user', lazy='dynamic')
    receiveMsgs = db.relationship('Message', backref='user', lazy='dynamic')

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10), unique = True)
    count = db.Column(db.Integer)
    time = db.Column(db.String(50))
    creator = db.Column(db.Integer)
    users = db.relationship('User', backref='team', lazy='dynamic')

class Apply(db.Model):
    __tablename__ = 'applys'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
