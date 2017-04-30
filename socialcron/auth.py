# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen
from socialcron import api_data as api
import json

class Auth(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def generate_token(self):
        url = "oauth/token?username=%s&password=%s&grant_type=password" %(self.username, self.password)
        auth_request = Request(api.BASE_URL + url)
        auth_request.add_header("Authorization", api.API_CREDENTIAL)
        auth_response = json.loads(urlopen(auth_request, data="").read())
        token = {"access_token": auth_response['access_token'],
                 "refresh_token": auth_response['refresh_token'],
                 "timeout": auth_response['expires_in']}
        self.token = token
        return token

    def renew_token(self):
        url = "oauth/token?grant_type=refresh_token&refresh_token=%s" %(self.token['refresh_token'])
        refresh_request = Request(api.BASE_URL + url)
        refresh_request.add_header("Authorization", api.API_CREDENTIAL)
        refresh_request = json.loads(urlopen(refresh_request, data="").read())
        token = {"access_token": refresh_request['access_token'],
                 "refresh_token": refresh_request['refresh_token'],
                 "timeout": refresh_request['expires_in']}
        self.token = token
        return token
