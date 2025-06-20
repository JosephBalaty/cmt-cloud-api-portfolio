import properties as p
import requests
from http import HTTPStatus
from exceptions import *
from six.moves.urllib.request import urlopen
from jose import jwt
from authlib.integrations.flask_client import OAuth
from flask import Flask, request, send_file, jsonify
from google.cloud import storage
import io
from google.cloud import datastore
from google.cloud.datastore.query import PropertyFilter
import json



class CourseInstructorDAO:
    def __init__(self):
        self.client = datastore.Client()
        self.storage_client = storage.Client()
    
    def post_course_instructor(self, course_id, instructor_id):
        instructor_key = self.client.key(p.COURSE_INSTRUCTOR)
        new_course_instructor = datastore.Entity(key=instructor_key)
        new_course_instructor.update({
            'instructor_id': instructor_id,
            'course_id': course_id
        })
        self.client.put(new_course_instructor)
    
    def patch_course_instructor(self, course_id, instructor_id):
        enrollment_query = self.client.query(kind=p.COURSE_INSTRUCTOR)
        enrollment_query.add_filter(filter=PropertyFilter(p.INSTRUCTOR_ID, '=', instructor_id))
        enrollment_query.add_filter(filter=PropertyFilter(p.COURSE_ID, '=', course_id))
        i_new = list(enrollment_query.fetch())[0]

        i_new.update({
            p.INSTRUCTOR_ID: instructor_id
        })