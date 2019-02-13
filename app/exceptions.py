class BaseException(Exception):
    status_code = 500
    message = 'internal server error'

    def __init__(self, message=None, status_code=None, payload=None):
        print(message)
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class WriterOnlyException(BaseException):
    status_code = 403
    message = 'writer only'


class NotFoundException(BaseException):
    status_code = 404
    message = 'not found'


class UnauthorizedException(BaseException):
    status_code = 401
    message = 'unauthorized'
