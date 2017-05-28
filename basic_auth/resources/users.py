from flask import current_app
from flask_restful import Resource, reqparse, marshal_with
from flask_restful_swagger import swagger
from basic_auth.models.users import get_verified_users, create_user, get_user_by_id, delete_user_by_id
from basic_auth.schemes import UserList, User
from basic_auth.exceptions import InternalError, UserNotFound
from basic_auth.helpers.decorators import requires_auth

get_user_parser = reqparse.RequestParser()
get_user_parser.add_argument('verified', type=int, location='args')
get_user_parser.add_argument('role_id', type=int, location='args')

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username', type=str)
create_user_parser.add_argument('email', type=str)
create_user_parser.add_argument('password', type=str)

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('username', type=str)
update_user_parser.add_argument('email', type=str)
update_user_parser.add_argument('password', type=str)

get_single_user_parser = reqparse.RequestParser()
get_single_user_parser.add_argument('user_id', type=int)


class UserListAPI(Resource):
    """docstring for Users"""
    decorators = [requires_auth]

    @swagger.operation(
        notes="""Retrieve list of users""",
        parameters=[
            {
                "name": "X-SESSION-ID",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            },
            {
                "name": "verified",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": "integer",
                "paramType": "query"
            },
            {
                "name": "role_id",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": "integer",
                "paramType": "query"
            }
        ],
        responseClass=UserList.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
        ]
    )
    @marshal_with(UserList.resource_fields)
    def get(self):
        "get list user"
        args = get_user_parser.parse_args()
        users = get_verified_users(args.get('verified', 1), args.get('role_id', None))
        return {'users': users}


class UserCreatingAPI(Resource):
    """docstring for UserCreatingAPI"""

    @swagger.operation(
        notes="""Add user / registered new user""",
        parameters=[
            {
                "name": "user",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": User.__name__,
                "paramType": "body"
            }
        ],
        responseClass=User.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
        ]
    )
    # @requires_auth
    @marshal_with(User.resource_fields)
    def post(self):
        "create user"
        args = create_user_parser.parse_args()
        user_data = {
            'username': args['username'],
            'email': args['email'],
            'password': args['password'],
        }
        user = create_user(user_data)
        return user


class UserAPI(Resource):
    """docstring for UserAPI"""
    decorators = [requires_auth]

    @swagger.operation(
        notes="""Retrieve users by user_id""",
        parameters=[
            {
                "name": "X-SESSION-ID",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            },
            {
                "name": "user_id",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path"
            }
        ],
        responseClass=User.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
        ]
    )
    @marshal_with(User.resource_fields)
    def get(self, user_id=None):
        "get user by id"
        users = get_user_by_id(user_id)
        if users:
            return users.view()
        return []

    @swagger.operation(
        notes="""Delete users by user_id""",
        parameters=[
            {
                "name": "X-SESSION-ID",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            },
            {
                "name": "user_id",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path"
            }
        ],
        responseClass=User.__name__,
        responseMessages=[
            {
                "code": 204,
                "message": "OK"
            },
        ]
    )
    @marshal_with(User.resource_fields)
    def delete(self, user_id=None):
        "delete user by id"
        try:
            delete_user_by_id(user_id)
        except InternalError:
            current_app.logger.error("Something went wrong deleting  user {} from coaching database".format(user_id))
            raise InternalError
        return 'no content', 204

    @swagger.operation(
        notes="""Update users by user_id""",
        parameters=[
            {
                "name": "X-SESSION-ID",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            },
            {
                "name": "user_id",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path"
            },
            {
                "name": "user",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": User.__name__,
                "paramType": "body"
            }
        ],
        responseClass=User.__name__,
        responseMessages=[
            {
                "code": 204,
                "message": "OK"
            },
        ]
    )
    @marshal_with(User.resource_fields)
    def put(self, user_id):
        "update user by id"
        args = update_user_parser.parse_args()
        user = get_user_by_id(user_id)
        if user is None:
            return UserNotFound
        if args['username']:
            if user.username != args['username']:
                user.username = args['username']
        if args['email']:
            if user.email != args['email']:
                user.email = args['email']
        if args['password']:
            if user.password != args['password']:
                user.password = args['password']
        user.save()
        return user.view()
