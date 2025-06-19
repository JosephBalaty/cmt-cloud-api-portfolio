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



class CourseDAO:
    def __init__(self):
        self.client = datastore.Client()
        self.storage_client = storage.Client()

    def post_course(self, content):
        new_key = self.client.key(p.COURSES)
        new_course = datastore.Entity(key=new_key)
        new_course.update({
            'subject': content['subject'],
            'number': int(content['number']),
            'title': content['title'],
            'term': content['term'],
            'instructor_id': int(content['instructor_id'])
        })

        self.client.put(new_course)
        new_course['id'] = new_course.key.id
        new_course['self'] = f'{request.url}/{new_course['id']}'

        return new_course