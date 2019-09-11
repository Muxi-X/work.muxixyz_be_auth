from flask import jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import Team, User, Apply
from ..decorator import login_required

import requests
import os
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
    usr = User.query.filter_by(email=email).first()

    if usr is None:
        usr = User(
                name=name,
                email=email,
                tel=tel
            )
        db.session.add(usr)
        db.session.commit()
        usr = User.query.filter_by(email=email).first()
        # 用户默认avatar
        usr.avatar = AVATARURL.format((usr.id%AVATARALL) + 1)

        record = Apply(user_id=usr.id)
        db.session.add(record)
        db.session.commit()
        if Team.query.filter_by(id=1).first() is None:
            muxi = Team(name="muxi", count=0, creator=1)
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
    user_email = request.get_json().get('email')
    token_string = request.get_json().get('token')
    status = check_pass2_auth(user_email, token_string)
    if status != 200:
        return jsonify({
            "reason": "check token error."
        }), 500
    else:
        usr = User.query.filter_by(email=user_email).first()
        if usr is None:
            return jsonify({
                "message": "user not found."
            }), 404
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


def check_pass2_auth(email, token):
    session = requests.Session()
    session.headers = {
        "content-type": "application/json"
    }
    scheme = ["http://", "https://"]
    domain_name = os.getenv("WORKBENCH_PASS2_DOMAIN", "pass2.muxixyz.com")
    path = "/auth/api/check_token?token={}&&email={}"

    response = session.get(scheme[0]+domain_name+path.format(token, email))
    print(scheme[0]+domain_name+path.format(token, email), response.status_code)
    return response.status_code
