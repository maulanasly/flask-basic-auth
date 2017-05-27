from functools import wraps
from flask import request
from basic_auth.models.users import get_session_by_id
from basic_auth.exceptions import MissingSessionID, UnAuthorized, SessionExpired


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        session_id = request.headers.get('X-SESSION-ID', None)
        if session_id is None:
            raise MissingSessionID
        else:
            session = get_session_by_id(session_id)
            if session is None:
                raise UnAuthorized
            if session.is_expired:
                raise SessionExpired
        return f(*args, **kwargs)
    return decorated
