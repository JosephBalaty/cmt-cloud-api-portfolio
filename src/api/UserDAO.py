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



class UserDAO:

    def __init__(self):
        self.client = datastore.Client()


    def verify_jwt(self, request):
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization'].split()
            token = auth_header[1]
        else:
            raise AuthError({"code": "no auth header",
                                "description":
                                    "Authorization header is missing"}, HTTPStatus.UNAUTHORIZED)
        
        jsonurl = urlopen("https://" + p.DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Invalid header. "
                                "Use an RS256 signed JWT Access Token"}, HTTPStatus.UNAUTHORIZED)
        if unverified_header["alg"] == "HS256":
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Invalid header. "
                                "Use an RS256 signed JWT Access Token"}, HTTPStatus.UNAUTHORIZED)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=p.ALGORITHMS,
                    audience=p.CLIENT_ID,
                    issuer="https://"+ p.DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, HTTPStatus.UNAUTHORIZED)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    " please check the audience and issuer"}, HTTPStatus.UNAUTHORIZED)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, HTTPStatus.UNAUTHORIZED)

            return payload
        else:
            raise AuthError({"code": "no_rsa_key",
                                "description":
                                    "No RSA key in JWKS"}, HTTPStatus.UNAUTHORIZED)

    def login(self, login_info):
        body = {
                'grant_type' : 'password',
                'username' : login_info["username"],
                'password' : login_info["password"],
                'client_id' : p.CLIENT_ID,
                'client_secret' : p.CLIENT_SECRET
            }
        headers = { 'content-type': 'application/json' }
        url = 'https://' + p.DOMAIN + '/oauth/token'
        r = requests.post(url, json=body, headers=headers)
        return r


    def authenticate_user(self, payload):
        query = self.client.query(kind=p.USERS)
        query.add_filter('sub', '=', payload['sub'])
        user = list(query.fetch())[0]
        return user


    def get_users(self):
        query = self.client.query(kind=p.USERS)
        users = list(query.fetch())
        for u in users:
            u['id'] = u.key.id
        return users
    

    def get_user_by_id(self, user_id):
        user_key = self.client.key(p.USERS, user_id)
        if user_key == None: return None

        user = self.client.get(key=user_key)        
        if user:
            user['id'] = user.key.id

        return user
