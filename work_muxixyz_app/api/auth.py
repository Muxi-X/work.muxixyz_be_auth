from flask import jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import Team, User, Apply
from ..decorator import login_required

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

AVATARURL = 'https://static.muxixyz.com/workbench/avatar/{}.png'
# 头像总数14个，因此%14 +1
AVATARALL = 14

@api.route('/auth/signup/', methods = ['POST'])
def signup():
    name = request.get_json().get('name')
    if name == "":
        return jsonify({"msg": "username can't be empty string"}), 402
    email = request.get_json().get('email')
    avatar = request.get_json().get('avatar')
    tel = request.get_json().get('tel')
    usr = User.query.filter_by(name = name).first()
    usR = User.query.filter_by(email = email).first()
    if (usr is None) and (usR is None):

        usr = User(
                name = name,
                email = email,
                tel = tel
            )
        db.session.add(usr)
        db.session.commit()
        usr = User.query.filter_by(name = name).first()
        # 用户默认avatar
        usr.avatar = AVATARURL.format((usr.id%AVATARALL) + 1)

        record = Apply(user_id = usr.id)
        db.session.add(record)
        db.session.commit()
        if Team.query.filter_by(id = 1).first() is None:
            muxi = Team(name = "muxi", count = 0, creator = 1)
            db.session.add(muxi)
            db.session.commit()
        response = jsonify({
            "msg": 'successful!',
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({
            "msg": 'user already existed!',
        })
        response.status_code = 401
        return response

@api.route('/auth/login/', methods=['POST'])
def login():
    usrname = request.get_json().get('name')
    usr = User.query.filter_by(email=usrname).first()
    if usr is None:
        response = jsonify({
            "msg": 'user not existed!',
        })
        response.status_code = 401
        return response
    else:
        if usr.avatar is None:
            usr.avatar = AVATARURL.format((usr.id % AVATARALL) + 1)
            db.session.add(usr)
            db.session.commit()
        token = usr.generate_confirmation_token()
        response = jsonify({
            "token": token,
            "uid": usr.id,
            "urole": usr.role,
        })
        response.status_code = 200
        return response
