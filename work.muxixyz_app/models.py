import time
from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class User(UserMixin,db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(20),unique=True)
	email=db.Column(db.String(35),unique=True)
	avatar=db.Column(db.String(50))
	tel=db.Column(db.String(15))
	role=db.Column(db.Integer)
	teamID=db.Column(db.Integer,db.ForeignKey('teams.id'))
	groupID=db.Column(db.Integer,db.ForeignKey('groups.id'))
	status=db.relationship('Statu',backref='user',lazy='dynamic')
	receiveMsgs=db.relationship('Comment',backref='user',lazy='dynamic')

	def generate_auth_token(self,expiration):
        s=Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'id':self.id})
    @staticmethod
    def verify_auth_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return None
        return User.query.get(data['id'])
    def generate_confirmation_token(self,expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')
    def confirm(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm')!=self.id:
            return False
        self.confirm=True
        db.session.add(self)
        return True

class Team(db.Model):
	__tablename__='teams'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(10),unique=True)
	count=db.Column(db.Integer)
	time=db.Column(db.String(50))
	creator=db.Column(db.Integer)

class Group(db.Model):
	__tablename__='groups'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(10),unique=True)
	count=db.Column(db.Integer)
	leader=db.Column(db.Integer)

class Project(db.Model):
	__tablename__='projects'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(10),unique=True)
	intro=db.Column(db.String)
	time=db.Column(db.String(50))
	count=db.Column(db.Integer)
	teamID=db.Column(db.Integer,db.ForeignKey('teams.id'))
	files=db.relationship('File',backref='project',lazy='dynamic')

class User2Project(db.Model):
	__tablename__='user2projects'
	id=db.Column(db.Integer,primary_key=True)
	userID=db.Column(db.Integer)
	projectID=db.Column(db.Integer)

class Statu(db.Model):
	__tablename__='status'
	id=db.Column(db.Integer,primary_key=True)
	content=db.Column(db.String)
	time=db.Column(db.String(50))
	like=db.Column(db.Integer)
	comment=db.Column(db.Integer)
	userID=db.Column(db.Integer,db.ForeignKey('users.id'))
	comments=db.relationship('Comment',backref='statu',lazy='dynamic')

class File(db.Model):
	__tablename__='files'
	id=db.Column(db.Integer,primary_key=True)
	url=db.Column(db.String,unique=True)
	path=db.Column(db.String)
	filename=db.Column(db.String)
	creator=db.Column(db.Integer)
	editor=db.Column(db.Integer)
	kind=db.Column(db.Boolean,default=False)
	projectID=db.Column(db.Integer,db.ForeignKey('projetcs.id'))
	comments=db.relationship('Comment',backref='file',lazy='dynamic')

class Comment(db.Model):
	__tablename__='comments'
	id=db.Column(db.Integer,primary_key=True)
	kind=db.Column(db.Integer)
	content=db.Column(db.String)
	time=db.Column(db.String(50))
	creator=db.Column(db.Integer)
	fileID=db.Column(db.Integer,db.ForeignKey('files,id'),default=0)
	statuID=db.Column(db.Integer,db.ForeignKey('status.id'),default=0)

class Message(db.Model):
	__tablename__='messages'
	id=db.Column(db.Integer,primary_key=True)
	time=db.Column(db.String)
	action=db.Column(db.String)
	kind=db.Column(db.Integer)
	readed=db.Column(db.Boolean,default=False)
	fromID=db.Column(db.Integer)
	receiveID=db.Column(db.Integer,db.ForeignKey('users.id'))
	fileID=db.Column(db.Integer,db.ForeignKey('files.id'),default=0)
	statuID=db.Column(db.Integer,db.ForeignKey('status.id'),default=0)
	commenID=db.Column(db.Integer,db.ForeignKey('comments.id'),default=0)
