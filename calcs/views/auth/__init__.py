import flask_login

from views.auth.database import users as db

"""
def create_login_manager(app):
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    return login_manager
"""


class User(flask_login.UserMixin):
    def __init__(self, username, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email
        self.id = username

    def verify_user(self, db):
        return self.username in db

    def verify_password(self, password, db):
        assert self.verify_user()
        if db[self.username]['password'] == password:
            return True
        else:
            return False

