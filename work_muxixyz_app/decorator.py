from functools import wraps
from flask import abort
# import jwt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def login_required(f):
    @wraps(f):
        def decorated_function(*args,**kwargs):
            if not 'token' in request.headers:
                abort(401)
            usr=None
            t=request.headers['token'].encode('utf-8')
            s=Serializer(current_app.configp['SECRET_KEY'])
            try:
                data=s.loads(t.encode('utf-8'))
            except:
                abort(401)
            uid=data.get('confirm')
            return f(uid,*args,**kwargs)
    return decorated_function
