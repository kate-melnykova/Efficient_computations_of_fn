import json
from time import time

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_user, login_required, logout_user, current_user
from redis import Redis
from wtforms import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators

from views.auth import User
from redispy import get_connection


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Length(min=6, max=35),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Length(min=6, max=35)])


def generate_error_message(form_errors):
    error_message = f''
    for k, v in form_errors.items():
        error_message += f""" -- {k}: {v[0]} \n"""
    return error_message


auth = Blueprint('auth', __name__)


@auth.route('/login')
@auth.route('/register')
def register():
    regform = RegistrationForm(request.form)
    loginform = LoginForm(request.form)
    return render_template('register.html', regform=regform, loginform=loginform)


@auth.route('/registration/process', methods=['POST'])
def registration_process():
    assert request.method == 'POST'
    regform = RegistrationForm(request.form)
    if regform.validate():
        username = regform.username.data
        user = User(username=username, password=regform.password.data, email=regform.email.data)
        connection = get_connection(db=current_app.config['USER_DB'])
        if connection.get(username) is None:
            user_db = user.serialize()
            connection.set(username, json.dumps(user_db))
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Username already exists')
            return redirect(url_for('auth.register'))
    else:
        error_message = f"""Incorrect credentials: \n""" + generate_error_message(regform.errors)
        flash(error_message)
        return redirect(url_for('auth.register'))


@auth.route('/login/process', methods=['POST'])
def login_process():
    assert request.method == 'POST'
    loginform = LoginForm(request.form)
    if loginform.validate():
        username = loginform.username.data
        user_db = get_connection(db=current_app.config['USER_DB']).get(username)
        if user_db is not None:
            user = User.deserialize(user_db)
            if user.verify_password(loginform.password.data):
                user.last_login = time()
                user_db = user.serialize()
                get_connection(db=current_app.config['USER_DB']).set(username, json.dumps(user_db))
                login_user(user, remember=True)
                return redirect(url_for('index'))
            else:
                flash(f"""Incorrect password \n""" + generate_error_message(loginform.errors))
                return redirect(url_for('auth.register'))
        else:
            flash(f"""The username does not exist: \n""" + generate_error_message(loginform.errors))
            return redirect(url_for('auth.register'))

    else:
        flash(f"""Incorrect credentials: \n""" + generate_error_message(loginform.errors))
        return redirect(url_for('auth.register'))


@auth.route("/logout")
@login_required
def logout():
    return render_template('logout.html')


@auth.route('/logout/process', methods=['POST'])
def logout_process():
    if request.form['response'] == 'yes':
        logout_user()
        flash('Successfully logged out')
        return redirect(url_for('auth.register'))
    else:
        return redirect(url_for('index'))




