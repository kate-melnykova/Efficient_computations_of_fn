from views.auth import User
from views.auth.database import users


def create_new_user(user):
    assert user.username not in users.keys()
    users[user.username] = {'password': user.password,
                            'email': user.email}


def validate_user(user):
    if user.username not in users:
        return False
    user_db = users[user.username]
    if user.password != user_db['password']:
        return False
    elif user.email is not None:
        return user.email == user_db['email']
