import json
from time import time

from views.auth import User
# from views.auth.database import users


def create_new_user(user, db):
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
