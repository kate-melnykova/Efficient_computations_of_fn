import json
from time import time

import flask_login
from werkzeug.security import generate_password_hash

# from views.auth.database import users as db


class User(flask_login.UserMixin):
    def set_password(self, password):
        self._password = generate_password_hash(password)

    # password = property(lambda self: self._password, set_password)

    def __init__(self, username, password, email=None, since=None, last_login=None):
        self.username = username
        self.email = email
        self.id = username
        self.password = password
        if since is None:
            cur_time = time()
            self.since = cur_time
            self.last_login = cur_time
        else:
            self.since = since
            self.last_login = last_login

    def convert_user_to_user_db(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'since': self.since,
            'last_login': self.last_login
        }

    def __str__(self):
        return f'{self.username} with email {self.email}'

    @staticmethod
    def convert_user_db_to_user(user_data):
        return User(**user_data)


def add_new_user(user, db):
    # assert user.username not in users.keys()
    assert db.get(user.username) is None
    # users[user.username] = {'password': user.password,
    #                         'email': user.email}
    cur_time = time()
    data = {
        'username': user.username,
        'password': user.password,
        'email': user.email,
        'since': cur_time,
        'last_login': cur_time
    }
    db.set(user.username, json.dumps(data))



