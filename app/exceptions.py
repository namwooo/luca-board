class BaseException(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class WriterOnly(BaseException):
    status_code = 403

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['writer'] = self.message
        return rv