import json
from time import time

import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

# from views.auth.database import users as db


class User(flask_login.UserMixin):
    def __str__(self):
        return f'{self.username} with email {self.email}'

    def __init__(self, username, password=None, email=None, since=None, last_login=None):
        self.username = username
        self.email = email
        self.id = username
        if len(password) < 40:
            self.password = generate_password_hash(password)
        else:
            # password is already hashed
            self.password = password
        if since is None:
            cur_time = time()
            self.since = cur_time
            self.last_login = cur_time
        else:
            self.since = since
            self.last_login = last_login

    def serialize(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'since': self.since,
            'last_login': self.last_login
        }

    def verify_password(self, password):
        print(self.password)
        return check_password_hash(self.password, password)

    @staticmethod
    def deserialize(user_data):
        user_data = json.loads(user_data)
        return User(**user_data)


def add_new_user(user, db):
    assert db.get(user.username) is None
    db.set(user.username, json.dumps(user.serialize()))



