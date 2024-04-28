import json


class UserInfo(object):
    def __init__(self, username: str = "", token: str = "", message: str = ""):
        self.username = username
        self.token = token
        self.message = message

    def set_username(self, username):
        self.username =username
    def set_token(self, token):
        self.token = token
    def get_username(self):
        jsonstr = json.loads(self.message)
        self.username = jsonstr['username']
        return self.username
    def get_token(self):
        return self.token

    def get_message(self):
        return self.message
    def set_message(self, message):
        self.message = message