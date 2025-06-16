import UserDAO


class UserService():
    userDao = UserDAO.UserDAO()

    @staticmethod
    def verify_login(request):
        login_info = request.get_json()

        if 'username' not in login_info or 'password' not in login_info:
            return p.MISSING_FIELDS, HTTPStatus.BAD_REQUEST
        
        reply = userDAO.login(login_info)

        if ('error' in reply):
            return p.UNAUTHORIZED_ERR, HTTPStatus.UNAUTHORIZED
        else:
            return {"token" : reply["id_token"]}, HTTPStatus.OK

    @staticmethod
    def get_users(request):
        try:
            payload = verify_jwt(request)
            user = userDao.authenticate_user(payload)
            if user['role'] != 'admin':
                return UNAUTHORIZED_ACCESS, HTTPStatus.FORBIDDEN
            else:
                return userDao.get_users()

        except AuthError as a:
            if a.error['code'] == 'invalid_header':
                return AUTHENTICATION_ERR, HTTPStatus.UNAUTHORIZED
        