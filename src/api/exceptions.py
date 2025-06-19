import properties as p
from http import HTTPStatus

class CMT_Base_Exception(Exception):
    pass

class AuthError(CMT_Base_Exception):
    def __init__(self, error=p.AUTHENTICATION_ERR, status_code=HTTPStatus.FORBIDDEN):
        self.error = error
        self.status_code = status_code


class BadRequest(CMT_Base_Exception):
    def __init__(self, error=p.MISSING_FIELDS, status_code=HTTPStatus.BAD_REQUEST):
        self.error = error
        self.status_code = status_code


class UnauthorizedAccess(CMT_Base_Exception):
    def __init__(self, error=p.UNAUTHORIZED_ACCESS, status_code=HTTPStatus.FORBIDDEN):
        self.error = error
        self.status_code = status_code 

class NotFound(CMT_Base_Exception):
    def __init__(self, error=p.MISSING_FILE_ERR, status_code=HTTPStatus.NOT_FOUND):
        self.error = error
        self.status_code = status_code 