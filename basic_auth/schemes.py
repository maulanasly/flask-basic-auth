from flask_restful import fields
from flask_restful_swagger import swagger


@swagger.model
class Auth(object):

    resource_fields = {
        'session_id': fields.String()
    }
    required = ['session_id']


@swagger.model
class UserAuth(object):

    resource_fields = {
        'username': fields.String(),
        'password': fields.String()
    }

    required = ['username', 'password']
