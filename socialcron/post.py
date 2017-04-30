# -*- coding: utf-8 -*-

import json
import urllib
from urllib2 import Request, urlopen, HTTPError
from socialcron import api_data as api

class Post(object):

    def __init__(self, title='', content='', id=-1):
        self.title = title
        self.content = content
        self.id = id

    def to_json(self):
        return json.dumps({"id": self.id, "title": self.title, "content": self.content})


class PostService(object):

    def __init__(self, auth):
        self.token = auth.token['access_token']

    def save(self, post):
        save_request = Request(api.BASE_URL + "v2/posts")
        save_request.add_header("Authorization", "Bearer %s" %(self.token))
        save_request.add_header("Content-Type", "application/json")

        try:
            response = urlopen(save_request, post.to_json())
            if response.getcode() == 201:
                return True
        except (HTTPError) as error:
            print error

        return False

    def find_one(self, id):
        find_request = Request(api.BASE_URL + "v2/posts/%s" %(id))
        find_request.add_header("Authorization", "Bearer %s" %(self.token))

        try:
            response_content = json.loads(urlopen(find_request).read())
            return Post(response_content['title'], response_content['content'], response_content['id'])
        except (HTTPError) as error:
            print error

    def find_all(self):
        find_request = Request(api.BASE_URL + "v2/posts/all")
        find_request.add_header("Authorization", "Bearer %s" %(self.token))

        try:
            response_content = json.loads(urlopen(find_request).read())
            posts = []

            for post in response_content:
                posts.append(Post(post['title'], post['content'], post['id']))

            return posts
        except (HTTPError) as error:
            print error

    def delete(self, id):
        delete_request = Request(api.BASE_URL + "v2/posts/%s" %(id))
        delete_request.add_header("Authorization", "Bearer %s" %(self.token))
        delete_request.get_method = lambda: 'DELETE'

        try:
            response = urlopen(delete_request)

            if response.getcode() == 204:
                return True

        except (HTTPError) as error:
            print error

        return False