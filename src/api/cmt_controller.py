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
import UserService


# INITIALIZATION

app = Flask(__name__)
oauth = OAuth(app)
client = datastore.Client()
userService = UserService.UserService()

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
@app.route('/' + p.USERS + '/login', methods=['POST'])
def user_login():
    print("Verifying login...")
    return userService.verify_login(request)

@app.route('/' + p.USERS, methods=['GET'])
def get_users():
    print("Getting users...")
    return userService.get_users(), HTTPStatus.OK