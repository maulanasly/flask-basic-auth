import json


class BaseExceptions(Exception):

    extra = dict()

    def __init__(self, **kwargs):
        super(BaseExceptions, self).__init__()
        for (key, value) in kwargs.iteritems():
            if key in self.extra_fields:
                self.extra[key] = value

    @classmethod
    def to_swagger(cls):
        reason = {
            "code": cls.code,
            "reason": cls.message,
            "extra_info": cls.extra_fields
        }
        return {
            "code": cls.status_code,
            "message": json.dumps(reason)
        }


class InvalidFileType(BaseExceptions):
    message = "Invalid file type"
    code = 100
    status_code = 400
    extra_fields = ['expected_type']


class MissingSessionID(BaseException):
    """docstring for MissingSessionID"""
    message = "required session id"
    code = 101
    status_code = 400
    extra_fields = ['message']


class UnAuthorized(BaseExceptions):
    message = "UnAuthorized User"
    code = 102
    status_code = 401
    extra_fields = ['expected_type']


class InvalidGoogleAUTH(BaseExceptions):
    message = "user is not valid"
    code = 103
    status_code = 401
    extra_fields = ['expected_type']


class SessionExpired(BaseExceptions):
    message = "session has expired"
    code = 104
    status_code = 401
    extra_fields = ['message']


class UserNotFound(BaseExceptions):
    message = "UnAuthorized User"
    code = 105
    status_code = 404
    extra_fields = ['message']


class InternalError(BaseExceptions):
    message = "Unknown error"
    code = 700
    status_code = 500
    extra_fields = ['message']
