import UserDAO, CourseDAO, CourseInstructorDAO
from http import HTTPStatus
import properties as p
from exceptions import *
import io


class CourseService():


    def __init__(self):
        self.userDao = UserDAO.UserDAO()
        self.courseDao = CourseDAO.CourseDAO()
        self.courseInstructorDao = CourseInstructorDAO.CourseInstructorDAO()
    

    def post_course(self, request):
        payload = self.userDao.verify_jwt(request)
        content = request.get_json()

        user = self.userDao.authenticate_user(payload)
        if (user['role'] != 'admin'):
            raise UnauthorizedAccess()
        
        if ('instructor_id' not in content or
            'subject' not in content or
            'number' not in content or
            'title' not in content or
            'term' not in content):
            raise BadRequest()

        instr_id = int(content['instructor_id'])
        instructor = self.userDao.get_user_by_id(instr_id)
        if (instructor == None or instructor['role'] != 'instructor'):
            raise BadRequest()
        
        new_course = self.courseDao.post_course(content)
        crs_id = new_course['id']
        self.courseInstructorDao.post_course_instructor(crs_id, instr_id)
        return new_course, HTTPStatus.CREATED