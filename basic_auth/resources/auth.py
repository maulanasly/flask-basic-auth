from flask import current_app
from flask_restful import Resource, reqparse, marshal_with
from flask_restful_swagger import swagger
from basic_auth.schemes import Auth, UserAuth, OAuth2
from basic_auth.models.users import get_user, get_session_by_user_id, generate_session, update_session
from basic_auth.exceptions import UnAuthorized, InvalidGoogleAUTH
from basic_auth import oauth

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', type=str, required=True)
auth_parser.add_argument('password', type=str, required=True)


class AuthAPI(Resource):
    """docstring for AuthAPI"""

    @swagger.operation(
        notes="""User authentication method""",
        parameters=[
            {
                "name": "payloads",
                "description": "",
                "required": True,
                "allowMultiple": False,
                "dataType": UserAuth.__name__,
                "paramType": "body"
            }
        ],
        responseClass=Auth.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
        ]
    )
    @marshal_with(Auth.resource_fields)
    def post(self):
        "authenticate user"
        args = auth_parser.parse_args()
        username = args['username']
        password = args['password']

        user = get_user(username)
        if user is not None:
            if user.bcrypt_password == password:
                session = get_session_by_user_id(user.user_id)
                if session is None:
                    session = generate_session(user.user_id)
                if session.is_expired:
                    session = update_session(user.user_id)
            else:
                return UnAuthorized
        else:
            return UnAuthorized
        return {'session_id': session.session_id}, 200
