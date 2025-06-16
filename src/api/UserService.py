import UserDAO
from http import HTTPStatus
import properties as p
from exceptions import *

class UserService():

    def __init__(self):
        self.userDao = UserDAO.UserDAO()

    def verify_login(self, request):
        login_info = request.get_json()

        if ('username' not in login_info or
            'password' not in login_info):
            return p.MISSING_FIELDS, HTTPStatus.BAD_REQUEST
        
        reply = self.userDao.login(login_info)

        if ('error' in reply):
            return p.AUTHENTICATION_ERR, HTTPStatus.UNAUTHORIZED
        else:
            return {"token" : reply["id_token"]}, HTTPStatus.OK

    def get_users(self, request):
        try:
            payload = self.userDao.verify_jwt(request)
            user = self.userDao.authenticate_user(payload)
            if user['role'] != 'admin':
                return p.UNAUTHORIZED_ACCESS, HTTPStatus.FORBIDDEN
            else:
                return self.userDao.get_users()

        except AuthError as a:
            if a.error['code'] == 'invalid_header':
                return p.AUTHENTICATION_ERR, HTTPStatus.UNAUTHORIZED
    
    def get_user_by_id(self, request, user_id):
        try:
            payload = self.userDao.verify_jwt(request)
            cur_user = self.userDao.authenticate_user(payload)
            searched_user = self.userDao.get_user_by_id(user_id)

            if (searched_user == None or 
                (   (cur_user['role'] != 'admin') and 
                    (cur_user.key.id != searched_user.key.id) )):

                print(searched_user, cur_user['role'], 
                    cur_user.key.id)
                return p.UNAUTHORIZED_ACCESS, HTTPStatus.FORBIDDEN



            """
            user_avatar_query = client.query(kind=USER_AVATAR)
            user_avatar_query.add_filter(filter=PropertyFilter('user_id', '=', user_id))
            results = list(user_avatar_query.fetch())

            if len(results) == 1:
                searched_user['avatar_url'] = f'{request.url}/{AVATAR}'
            
            courses = []

            if cur_user['role'] == 'admin':
                return searched_user
            
            elif cur_user['role'] == 'instructor':
                course_instructor_query = client.query(kind=COURSE_INSTRUCTOR)
                course_instructor_query.add_filter(filter=PropertyFilter('instructor_id', '=', user_id))
                courses_taught = list(course_instructor_query.fetch())
                for c in courses_taught:
                    courses.append(f'{request.root_url}{COURSES}/{c['course_id']}')
                searched_user['courses'] = courses

            else:
                enrollment_query = client.query(kind=ENROLLMENT)
                enrollment_query.add_filter(filter=PropertyFilter('student_id', '=', user_id))
                courses_enrolled = list(enrollment_query.fetch())
                for c in courses_enrolled:
                    courses.append(f'{request.root_url}{COURSES}/{c['course_id']}')
                searched_user['courses'] = courses
            """

            return searched_user

        except AuthError as a:
            if a.error['code'] == 'invalid_header':
                return p.AUTHENTICATION_ERR, HTTPStatus.UNAUTHORIZED