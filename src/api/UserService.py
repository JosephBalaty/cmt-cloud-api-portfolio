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
            raise BadRequest(p.MISSING_FIELDS, HTTPStatus.BAD_REQUEST)

        reply = self.userDao.login(login_info)
        reply = reply.raise_for_status().json()
        return {"token" : reply["id_token"]}, HTTPStatus.OK

    def get_users(self, request):
        payload = self.userDao.verify_jwt(request)
        user = self.userDao.authenticate_user(payload)
        if user['role'] != 'admin':
            raise UnauthorizedAccess(p.UNAUTHORIZED_ACCESS, HTTPStatus.FORBIDDEN)
        else:
            return self.userDao.get_users()

    def get_user_by_id(self, request, user_id):
        payload = self.userDao.verify_jwt(request)
        cur_user = self.userDao.authenticate_user(payload)
        searched_user = self.userDao.get_user_by_id(user_id)

        if (searched_user == None or 
            (   (cur_user['role'] != 'admin') and 
                (cur_user.key.id != searched_user.key.id) )):
            raise UnauthorizedAccess(p.UNAUTHORIZED_ACCESS, HTTPStatus.FORBIDDEN)


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


    def store_avatar(request):
        # Any files in the request will be available in request.files object
        # Check if there is an entry in request.files with the key 'file'
        if 'file' not in request.files:
            print(request.files)
            return MISSING_FIELDS, 400

        payload = verify_jwt(request)

        query = client.query(kind=USERS)
        query.add_filter('sub', '=', payload['sub'])
        user = list(query.fetch())[0]

        if user.key.id != user_id:
            return UNAUTHORIZED_ACCESS, 403
        # Set file_obj to the file sent in the request
        file_obj = request.files['file']
        # Create a storage client
        storage_client = storage.Client()
        # Get a handle on the bucket
        bucket = storage_client.get_bucket(PHOTO_BUCKET)
        # Create a blob object for the bucket with the name of the file
        blob = bucket.blob(file_obj.filename)
        # Position the file_obj to its beginning
        file_obj.seek(0)

        # check if there is already an avatar for the user. if so, delete
        # the old avatar and insert the new one.
        user_avatar_query = client.query(kind=USER_AVATAR)
        user_avatar_query.add_filter(filter=PropertyFilter('user_id', '=', user_id))
        results = list(user_avatar_query.fetch())

        if len(results) == 1:
            # remove the current file and then delete this result.
            user_avatar = results[0]
            old_avatar_id = user_avatar['avatar_id']
            blobs = storage_client.list_blobs(PHOTO_BUCKET)
            for b in blobs:
                if old_avatar_id == b.id:
                    b.delete()
                    break
            client.delete(user_avatar)


        # Upload the file into Cloud Storage
        blob.upload_from_file(file_obj)
        # update our user_avatar table with the id from the new file_obj.
        user_avatar_key = client.key(USER_AVATAR)
        new_user_avatar = datastore.Entity(key=user_avatar_key)
        new_user_avatar.update({
            'user_id': user_id,
            'avatar_id': blob.id
        })
        client.put(new_user_avatar)


        resp = {}
        resp['avatar_url'] = request.url
        return resp