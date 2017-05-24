class BaseExceptions(Exception):

    extra = dict()

    def __init__(self, **kwargs):
        super(BaseExceptions, self).__init__()
        for (key, value) in kwargs.iteritems():
            if key in self.extra_fields:
                self.extra[key] = value


class InvalidFileType(BaseExceptions):
    message = "Invalid file type"
    code = 100
    status_code = 400
    extra_fields = ['expected_type']


class UnAuthorized(BaseExceptions):
    message = "UnAuthorized User"
    code = 101
    status_code = 401
    extra_fields = ['expected_type']


class UserNotFound(BaseExceptions):
    message = "UnAuthorized User"
    code = 102
    status_code = 404
    extra_fields = ['message']


class InternalError(BaseExceptions):
    message = "Unknown error"
    code = 700
    status_code = 500
    extra_fields = ['message']
