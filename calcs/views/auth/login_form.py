from flask import Flask
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
import flask_login
from flask_login import login_user, login_required, logout_user
from flask_login import LoginManager
from wtforms import Form
from wtforms import BooleanField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators

from views.auth import User
from views.auth.database import users
from views.auth.db_methods import create_new_user


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [validators.DataRequired()])

    def validate_user(self, db):
        user = User(username=self.username.data, password=self.password.data)
        self.errors = ''
        if not user.verify_user(self, db):
            self.errors = 'Unknown username'
            return False
        if not user.verify_password(self.password.data):
            self.errors('Invalid password')
            return False
        return True


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    regform = RegistrationForm(request.form)
    loginform = LoginForm(request.form)
    message_register = ''
    message_login = ''
    if request.method == 'POST':
        if request.form['submit'] == 'Register':
            if regform.validate():
                username = request.form['username']
                password = request.form['password']
                email = request.form['email']
                user = User(username=username, password=password, email=email)
                if username in users:
                    return render_template('register.html',
                                           regform=regform,
                                           loginform=loginform,
                                           message_register='Username already exists',
                                           login_register='')
                else:
                    create_new_user(user)
                    login_user(user)
                    return redirect(url_for('index'))
            else:
                return render_template('register.html',
                                       regform=regform,
                                       loginform=loginform,
                                       message_register='Too short password',
                                       login_register='')
        elif request.form['submit'] == 'Login':
            if loginform.validate():
                username = request.form['username']
                password = request.form['password']
                user = User(username=username, password=password, email='')
                if username in users:
                    # login user
                    login_user(user)
                    flash('Login is successful')
                    return redirect(url_for('index'))
                else:
                    return render_template('register.html',
                                           regform=regform,
                                           loginform=loginform,
                                           message_register='',
                                           login_register='Username already exists')

    else:
        return render_template('register.html',
                               regform=regform,
                               loginform=loginform,
                               message_register='',
                               login_register='')


@auth.route('/registration_process', methods=['POST'])
def registration_process():
    return 'Registration is successful'


@auth.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'GET':
        return render_template('logout.html')
    else:
        if request.form['response'] == 'yes':
            logout_user()
            flash('You have successfully logged out')
        return redirect(url_for('index'))



