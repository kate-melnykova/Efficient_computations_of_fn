from flask_wtf import FlaskForm, RecaptchaField
from wtforms import TextField


class SignupForm(FlaskForm):
    username = TextField('Username')
    recaptcha = RecaptchaField()