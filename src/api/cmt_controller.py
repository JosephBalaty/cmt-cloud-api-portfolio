from flask import Flask, request, send_file, jsonify


from google.cloud import storage
from google.cloud import datastore
from google.cloud.datastore.query import PropertyFilter

import requests
import json
import io
from six.moves.urllib.request import urlopen
from jose import jwt
from authlib.integrations.flask_client import OAuth
from http import HTTPStatus

import properties as p
import UserService, CourseService
from exceptions import *


# INITIALIZATION

app = Flask(__name__)
oauth = OAuth(app)
userService = UserService.UserService()
courseService = CourseService.CourseService()

auth0 = oauth.register(
    'auth0',
    client_id=p.CLIENT_ID,
    client_secret=p.CLIENT_SECRET,
    api_base_url="https://" + p.DOMAIN,
    access_token_url="https://" + p.DOMAIN + "/oauth/token",
    authorize_url="https://" + p.DOMAIN + "/authorize",
    client_kwargs={
        'scope': 'openid profile email',
    },
)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


# ROUTE HANDLERS

@app.route('/' + p.USERS + '/' + p.LOGIN, methods=['POST'])
def user_login():
    print("Verifying login...")
    return userService.verify_login(request), HTTPStatus.OK


@app.route('/' + p.USERS, methods=['GET'])
def get_users():
    print("Getting users...")
    return userService.get_users(request), HTTPStatus.OK


@app.route('/' + p.USERS + '/{p.PATH_VARIABLE_INT_USER_ID}', methods=['GET'])
def get_user_by_id(user_id):
    print(f'Getting user {user_id}...')
    return userService.get_user_by_id(request, user_id), HTTPStatus.OK


@app.route('/' + p.USERS + '/{p.PATH_VARIABLE_INT_USER_ID}/' + p.AVATAR, methods=['POST'])
def store_avatar(user_id):
    print(f'Storing avatar for user {user_id}...')
    return userService.store_avatar(request, user_id), HTTPStatus.OK


@app.route('/' + p.USERS + '/{p.PATH_VARIABLE_INT_USER_ID}/' + p.AVATAR, methods=['GET'])
def get_avatar(user_id):
    print(f'Getting avatar for user {user_id}...')
    return userService.get_avatar(request, user_id), HTTPStatus.OK


@app.route('/' + p.USERS + '/{p.PATH_VARIABLE_INT_USER_ID}/' + p.AVATAR, methods=['DELETE'])
def delete_avatar(user_id):
    print(f'Deleting user {user_id}\' avatar...')
    return userService.delete_avatar(request, user_id), HTTPStatus.NO_CONTENT


@app.route('/' + p.COURSES, methods=['POST'])
def post_course():
    return courseService.post_course(request), HTTPStatus.CREATED


@app.route('/' + p.COURSES, methods=['GET'])
def get_courses():
    return courseService.get_courses(request), HTTPStatus.OK


@app.route('/' + p.COURSES + '/' + p.PATH_VARIABLE_INT_COURSE_ID, methods=['GET'])
def get_course(course_id):
    return courseService.get_course(request, course_id), HTTPStatus.OK


# EXCEPTION HANDLER
@app.errorhandler(CMT_Base_Exception)
def handle_cmt_errors(ex):
    print("Received an exception for:", ex.status_code, ex.error)
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response