from flask import jsonify,request,current_app,url_for
from . import api
from .. import db
from ..models import Team,Group,User,Project,Message,Statu,File,Comment

from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@api.route('/auth/signup/',methods=['POST'])
def signup():
    name=request.get_json().get('name')
    email=request.get_json().get('email')
#    avatar=request.get_json().get('avatar')
    tel=request.get_json().get('tel')
    usr=User.query.filter_by(name=name).first()
    if usr is None:
        usr=User(
                name=name,
                email=email,
                tel=tel,
            )
        db.session.add(usr)
        db.commit()
        response=jsonify({
            "msg": 'successful!',
        })
        response.status_code=200
        return response
    else:
        response=jsonify({
            "msg": 'user already existed!',
        })
        response.status_code=401
        return response

@api.route('/auth/login/',methods=['POST'])
def login():
    usrname=request.get_json().get('username')
    usr=User.query.filter_by(username=usrname).first()
    if usr is None:
        response=jsonify({
            "msg": 'user not existed!',
        })
        response.status_code=401
        return response
    else:
        token=usr.generate_confirmation_token()
        response=jsonify({
            "token": token,
        })
        response.status_code=200
        return response

@api.route('/auth/verify/',methods=['POST'])
def verify():
    t=request.get_json().get('token')
    s=Serializer(current_app.config['SECRET_KEY'])
    try:
        data=s.loads(t.encode('utf-8'))
    except:
        response=jsonify({})
        response.status_code=402
        return response
    uid=data.get('confirm')
    response=jsonify({
        "uid": uid,
    })
    response.status_code=200
    return response
