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
        if (user[p.ROLE] != p.ADMIN):
            raise UnauthorizedAccess()
        
        if (p.INSTRUCTOR_ID not in content or
            p.SUBJECT not in content or
            p.NUMBER not in content or
            p.TITLE not in content or
            p.TERM not in content):
            raise BadRequest()

        instr_id = int(content[p.INSTRUCTOR_ID])
        instructor = self.userDao.get_user_by_id(instr_id)
        if (instructor == None or instructor[p.ROLE] != p.INSTRUCTOR):
            raise BadRequest()
        
        new_course = self.courseDao.post_course(content)
        crs_id = new_course[p.ID]
        self.courseInstructorDao.post_course_instructor(crs_id, instr_id)
        return new_course

        
    def get_courses(self, request, offset=0, limit=3):
        if len(request.args) == 2:
            limit = int(request.args['limit'])
            offset = int(request.args['offset'])
        
        return self.courseDao.get_courses(limit, offset)


    def get_course(self, request, course_id):
        return self.courseDao.get_course(course_id, request.url)