import flask_login
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from views.auth.database import users as db

"""
def create_login_manager(app):
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    return login_manager
"""


class User(flask_login.UserMixin):
    def set_password(self, password):
        print(password, generate_password_hash(password))
        self._password = generate_password_hash(password)

    password = property(lambda self: self._password, set_password)

    def __init__(self, username, password, email=None):
        self.username = username
        self.email = email
        self.id = username
        self.password = password

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_user_exists(self, db=db):
        return self.username in db

    def verify_password_db(self, db=db):
        assert self.verify_user_exists(db=db)
        return db[self.username]['password'] == self.password



