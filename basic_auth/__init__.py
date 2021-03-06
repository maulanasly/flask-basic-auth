from flask import Flask, jsonify, request
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_sqlalchemy import SQLAlchemy
from basic_auth.exceptions import BaseExceptions, SessionExpired, MissingSessionID
from basic_auth.config import config
from flask_oauthlib.client import OAuth


import os


app = Flask(__name__, instance_relative_config=True)

environment = os.getenv('APP_CONFIGURATION', 'development')
config_file = environment + '.cfg'
app.config.from_object(config[environment])
app.config.from_pyfile(config_file, silent=True)

api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/spec', description="basic authentications")
db = SQLAlchemy(app)
oauth = OAuth(app)


from basic_auth.resources.auth import AuthAPI
from basic_auth.resources.users import UserListAPI, UserAPI, UserCreatingAPI


api.add_resource(AuthAPI, '/login')
api.add_resource(UserCreatingAPI, '/users')
api.add_resource(UserAPI, '/users/<string:user_id>')
api.add_resource(UserListAPI, '/users/list')


@app.errorhandler(BaseExceptions)
def handler_senseauth_exception(error):
    session_id = request.headers.get('X-SESSION-ID', None)
    if session_id:
        new_error = SessionExpired(session_id=session_id)
    else:
        new_error = MissingSessionID()
    data = {
        "code": new_error.code,
        "reason": new_error.message,
        "extra_info": new_error.extra
    }
    response = jsonify(data)
    response.status_code = new_error.status_code
    return response


@app.errorhandler(BaseExceptions)
def handle_exception(error):
    data = {
        "code": error.code,
        "reason": error.message,
        "extra_info": error.extra
    }
    response = jsonify(data)
    response.status_code = error.status_code
    return response
