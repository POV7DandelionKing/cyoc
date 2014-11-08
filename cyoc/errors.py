import json
from pyramid.httpexceptions import HTTPError
from pyramid.response import Response


class JSONError(HTTPError):
    code = 400
    errors = {'message': 'Bad Request'}

    def __init__(self, code=None, errors=None):
        if code:
            self.code = code
        if errors:
            self.errors = errors
        body = {
            'code': self.code,
            'errors': self.errors
            }
        Response.__init__(self, json.dumps(body))
        self.status = str(self.code)
        self.content_type = 'application/json'


class JSONUnauthorized(JSONError):
    code = 401
    errors = {'message': 'Unauthorized'}
