from views.auth import User
from views.auth.database import users


def create_new_user(user):
    assert user.username not in users.keys()
    users[user.username] = {'password': user.password,
                            'email': user.email}
