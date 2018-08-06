from flask import Blueprint

api=Blueprint("api",__name__)

from . import auth,management,feed,message,project,status
