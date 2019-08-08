import flask_login
from flask_login import login_manager
from wtforms import Form
from wtforms import BooleanField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators

from authentification import User


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


