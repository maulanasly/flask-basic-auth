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


@swagger.model
class OAuth2(object):

    resource_fields = {
        'user_info': fields.Raw()
    }
    required = []


@swagger.model
class User(object):
    """docstring for User"""

    resource_fields = {
        'user_id': fields.String(),
        'email': fields.String(),
        'username': fields.String(),
        'created_at': fields.DateTime()
    }

    required = ['email', 'username']


@swagger.model
@swagger.nested(
    users=User.__name__)
class UserList(object):
    """docstring for ClassName"""

    resource_fields = {
        "users": fields.List(fields.Nested(User.resource_fields))
    }

    required = ['users']
