import UserDAO
from http import HTTPStatus
import properties as p
from exceptions import *
import io


class UserService():

    def __init__(self):
        self.userDao = UserDAO.UserDAO()


    def verify_login(self, request):
        login_info = request.get_json()

        if ('username' not in login_info or
            'password' not in login_info):
            raise BadRequest()

        reply = self.userDao.login(login_info)
        reply = reply.raise_for_status().json()
        return {"token" : reply["id_token"]}, HTTPStatus.OK


    def get_users(self, request):
        payload = self.userDao.verify_jwt(request)
        user = self.userDao.authenticate_user(payload)
        if user['role'] != 'admin':
            raise UnauthorizedAccess()
        else:
            return self.userDao.get_users()


    def get_user_by_id(self, request, user_id):
        payload = self.userDao.verify_jwt(request)
        cur_user = self.userDao.authenticate_user(payload)
        searched_user = self.userDao.get_user_by_id(user_id)

        if (searched_user == None or 
            (   (cur_user['role'] != 'admin') and 
                (cur_user.key.id != searched_user.key.id) )):
            raise UnauthorizedAccess()


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


    def store_avatar(self, request, user_id):
        # Any files in the request will be available in request.files object
        # Check if there is an entry in request.files with the key 'file'
        if 'file' not in request.files:
            raise BadRequest(error=p.MISSING_FILE_ERR)

        payload = self.userDao.verify_jwt(request)
        user = self.userDao.authenticate_user(payload);

        if user.key.id != user_id:
            raise UnauthorizedAccess()

        result = self.userDao.get_user_avatar(user_id)
        if len(result) == 1:
            user_avatar = result[0]
            self.userDao.delete_avatar(user_avatar)

        self.userDao.create_user_avatar(request.files['file'], user_id)
        return { "avatar_url" : request.url }


    def get_avatar(self, request, user_id):
        payload = self.userDao.verify_jwt(request)
        user = self.userDao.authenticate_user(payload)

        if user.key.id != user_id:
            raise UnauthorizedAccess()

        
        # Create a file object in memory using Python io package
        file_obj = io.BytesIO()
        result = self.userDao.get_user_avatar(user_id)

        if len(result) == 1:
            avatar_id = result[0]['avatar_id']
            return self.userDao.download_avatar(avatar_id)
        else:
            raise NotFound()