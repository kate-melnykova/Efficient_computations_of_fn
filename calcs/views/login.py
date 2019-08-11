from flask import Blueprint
import flask_login

from views.authentification import User

login = Blueprint('login', __name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(login)

# Our mock database.
users = {'user1': {'password': 'pass1'}}


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User(username=username)
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    password = request.form.get('password')
    if username not in users:
        return

    user = User(username=username, password=password)

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[username]['password']

    return user

