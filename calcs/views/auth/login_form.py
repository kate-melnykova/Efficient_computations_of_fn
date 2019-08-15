from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_user, login_required, logout_user
from wtforms import Form
# from wtforms import BooleanField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators

from views.auth import User
# from views.auth.database import users
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
    password = PasswordField('Password', [validators.DataRequired()])


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
@auth.route('/register', methods=['GET'])
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
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    user = User(username=username, password=password, email=email)
    if user.verify_user_exists():
        flash('Username already exists')
        return redirect(url_for('auth.register'))
    else:
        create_new_user(user)
        login_user(user)
        return redirect(url_for('index'))


    # if request.form['submit'] == 'Register':
    #     if regform.validate():
    #         return redirect(url_for('registration_process'))
    #     else:
    #         flash("Passwords don't match")
    #         return render_template('register.html',
    #                                regform=regform,
    #                                loginform=loginform,
    #                                message_register="Passwords don't match",
    #                                login_register='')
    # else:
    #     if loginform.validate():
    #         return redirect(url_for('login_process'))
    #     else:
    #         flash("Incorrect username/password")
    #         return render_template('register.html',
    #                                regform=regform,
    #                                loginform=loginform,
    #                                message_register='',
    #                                login_register="Incorrect username/password")
    #

@auth.route('/login/process', methods=['POST'])
def login_process():
    assert request.method == 'POST'
    username = request.form['username']
    password = request.form['password']
    user = User(username=username, password=password, email='')
    if user.verify_user_exists():
        if user.verify_password_db():
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Incorrect password')
            return redirect(url_for('auth.register'))

    else:
        flash('Username already exists')
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




