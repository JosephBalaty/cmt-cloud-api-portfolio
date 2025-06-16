class CMT_Base_Exception(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

class AuthError(CMT_Base_Exception):
    pass


class BadRequest(CMT_Base_Exception):
    def __init(self):
        self.error = p.BAD_REQUEST
        self.status_code = 400


class UnauthorizedAccess(CMT_Base_Exception):
    pass