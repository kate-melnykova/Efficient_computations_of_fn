import json
from time import time

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_user, login_required, logout_user, current_user
from redis import Redis
from wtforms import Form
# from wtforms import BooleanField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators
# from werkzeug.security import check_password_hash

from views.auth import User
# from views.auth.database import users
from views.auth import add_new_user


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


auth = Blueprint('auth', __name__)

redis_connection_user = Redis(host='redis', port=6379, db=1)


@auth.route('/login')
@auth.route('/register')
def register():
    regform = RegistrationForm(request.form)
    loginform = LoginForm(request.form)
    return render_template('register.html',
                           regform=regform,
                           loginform=loginform,
                           message_register='',
                           login_register='')


@auth.route('/registration/process', methods=['POST'])
def registration_process():
    assert request.method == 'POST'
    regform = RegistrationForm(request.form)
    if regform.validate():
        username = regform.username.data
        user = User(username=username, password=regform.password.data, email=regform.email.data)
        if redis_connection_user.get(username) is None:
            user_db = user.convert_user_to_user_db()
            redis_connection_user.set(username, json.dumps(user_db))
            login_user(user)
            print(current_user)
            return redirect(url_for('index'))
        else:
            flash('Username already exists')
            return redirect(url_for('auth.register'))
    else:
        error_message = f"""Incorrect credentials: \n"""
        for k, v in regform.errors.items():
            error_message += f""" -- {k}: {v[0]} \n"""
            # print(error_message)
        flash(error_message)
        return redirect(url_for('auth.register'))


@auth.route('/login/process', methods=['POST'])
def login_process():
    assert request.method == 'POST'
    loginform = LoginForm(request.form)
    if loginform.validate():
        username = loginform.username.data
        user_db = redis_connection_user.get(username)
        if user_db is not None:
            print(f'User found: {user_db}')
            user_db = json.loads(user_db)
            user = User.convert_user_db_to_user(user_db)
            # if check_password_hash(user.password, loginform.password.data):
            if user.password == loginform.password.data:
                # login successful
                user.last_login = time()
                # login_user(user)
                user_db = user.convert_user_to_user_db()
                redis_connection_user.set(username, json.dumps(user_db))
                val = login_user(user, remember=True)
                print(current_user)
                return redirect(url_for('index'))
                # return render_template('index.html')
            else:
                error_message = f"""Incorrect password: \n"""
                for k, v in loginform.errors.items():
                    error_message += f""" -- {k}: {v[0]} \n"""
                    # print(error_message)
                flash(error_message)
                return redirect(url_for('auth.register'))
        else:
            error_message = f"""The username does not exist: \n"""
            for k, v in loginform.errors.items():
                error_message += f""" -- {k}: {v[0]} \n"""
                # print(error_message)
            flash(error_message)
            return redirect(url_for('auth.register'))

    else:
        error_message = f"""Incorrect credentials: \n"""
        for k, v in loginform.errors.items():
            error_message += f""" -- {k}: {v[0]} \n"""
            # print(error_message)
        flash(error_message)
        return redirect(url_for('auth.register'))


@auth.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'GET':
        return render_template('logout.html')
    else:
        return redirect(url_for('auth.logout_process'))


@auth.route('/logout/process', methods=['POST'])
def logout_process():
    if request.form['response'] == 'yes':
        logout_user()
        print('Logged out')
        return redirect(url_for('auth.register'))
    else:
        return redirect(url_for('index'))




