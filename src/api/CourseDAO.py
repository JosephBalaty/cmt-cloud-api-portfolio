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
            p.SUBJECT: content[p.SUBJECT],
            p.NUMBER: int(content[p.NUMBER]),
            p.TITLE: content[p.TITLE],
            p.TERM: content[p.TERM],
            p.INSTRUCTOR_ID: int(content[p.INSTRUCTOR_ID])
        })

        self.client.put(new_course)
        new_course[p.ID] = new_course.key.id
        new_course[p.SELF] = f'{request.url}/{new_course[p.ID]}'

        return new_course
    

    def get_courses(self, limit, offset):
        query = self.client.query(kind=p.COURSES)
        query.order = [p.SUBJECT]
        l_iterator = query.fetch(limit=limit, offset=offset)
        pages = l_iterator.pages
        results = list(next(pages))

        for r in results:
            r[p.ID] = r.key.id
            r[p.SELF] = f'{request.base_url}/{r[p.ID]}'

        reply = {}
        reply[p.COURSES] = results
        reply['next'] = f'{request.base_url}?offset={offset+limit}&limit={limit}'

        return reply
    
    def get_course(self, course_id, url):
        course_key = self.client.key(p.COURSES, course_id)
        course = self.client.get(key=course_key)

        if course == None:
            raise NotFound()
        else:
            course[p.ID] = course.key.id
            course[p.SELF] = url
            return course