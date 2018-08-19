from pathlib import Path
import unittest
import os
from work_muxixyz_app import create_app,db
from flask import current_app,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from work_muxixyz_app.models import Team,Group,User,Project,Message,Statu,File,Comment
import random
import json

# db=SQLAlchemy()

class BasicTestCase(unittest.TestCase):

    def get_api_headers(self,ifToken):
        if ifToken is True:
            return {
                'token': TOKEN,
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
        else:
            return {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }

    def setUp(self):
        self.app = create_app(os.getenv('FLASK_CONFIG') or 'default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

#    def tearDown(self):
#        db.session.remove()
#        db.drop_all()
#        db.create_all()
#        self.app_context.pop()

    def test_app_exist(self):
        self.assertFalse(current_app is None)

# API FOR AUTH START

    def test_auth_a_signup(self):
        response=self.client.post(
            url_for('api.signup',_external=True),
            data=json.dumps({
                "name": 'test',
                "email": 'test@test.com',
                "avatar": 'https://test/test.png',
                "tel": '11111111111',
            }),
            headers=self.get_api_headers(False),
        )
#        print( url_for('api.signup',_external=True) )
        self.assertTrue(response.status_code==200)

    def test_auth_b_login(self):
        response=self.client.post(
            url_for('api.login',_external=True),
            data=json.dumps({
                "username": 'test',
            }),
            headers=self.get_api_headers(False),
        )
        s=json.loads(response.data.decode('utf-8'))['token']
        global TOKEN
        TOKEN=s
#        print (TOKEN)
        self.assertTrue(response.status_code==200)

    def test_auth_c_verify(self):
#        print (TOKEN)
        response=self.client.post(
            url_for('api.verify',_external=True),
            headers=self.get_api_headers(True),
            data=json.dumps({
                "token": TOKEN,
            }),
        )
#        print (response.status_code)
        s=json.loads(response.data.decode('utf-8'))['uid']
        print ('ID:'+str(s)+ ' ')
        self.assertTrue(response.status_code==200)

# API FOR AUTH END
