from _get import Get
from _post import Post
from _put import Put
from _delete import Delete


class Actions(Get, Post, Put, Delete):
    def __init__(self, api_key, token):
        self.api_key = api_key
        self.token = token
