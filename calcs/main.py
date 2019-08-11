from time import time

from flask import Blueprint
from flask import flash
from flask import url_for
from flask import redirect
from flask import request
from flask import render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import json
from redis import Redis

from factory_app import factory_app
from views.auth import User
from views.auth.database import users
from views.auth.login_form import RegistrationForm, LoginForm
from views.auth.login_form import auth
from sci_funcs.tasks import args_to_function
from sci_funcs.function_registry import function_registry

app, celery, redis_connection = factory_app()

######
# LoginManager setup
######
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User(username=username)
    return user


app.register_blueprint(auth)

"""
@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user
"""


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/schedule_calculation', methods=['POST'])
def schedule_calculation():
    assert request.method == 'POST'

    func_name = request.form['func_name']
    assert func_name in function_registry

    arguments = dict()
    arguments['func_name'] = func_name
    arguments['status'] = 'IN PROGRESS'
    arguments['start_time'] = time()
    for item in function_registry[func_name][1:]:
        arguments[item] = request.form[item]

    # get task identifier
    async_result = args_to_function.delay(arguments, function_registry[func_name][1:])

    message = json.dumps({"status": "PENDING",
                          "result":  arguments,
                          "task_id": async_result.task_id
                          })
    redis_connection.set(f'celery-task-meta-{async_result.task_id}', message)
    return redirect(url_for('view_results'))


@app.route('/view_results', methods=['GET'])
def view_results():
    results_temp = {}
    for key in redis_connection.keys('*'):
        result = json.loads(redis_connection.get(key))
        task_id = result['task_id']
        result = result['result']
        results_temp[task_id] = result

    return render_template('view_results.html',
                           results=results_temp)


@app.route('/result', methods=['GET'])
@login_required
def view_specific_results():
    task_id = str(request.args.get('task_id', ''))
    key = str.encode('celery-task-meta-' + task_id)
    try:
        result = json.loads(redis_connection.get(key))
    except:
        flash('Task not found')
        return redirect(url_for('index'))

    result = result['result']
    return render_template(f'{ result["func_name"] }.html',
                           result=result)
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    regform = RegistrationForm(request.form)
    loginform = LoginForm(request.form)
    message_register = ""
    message_login = ""
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
                    return redirect(url_for('registration_process'))
            else:
                return render_template('register.html',
                                       regform=regform,
                                       loginform=loginform,
                                       message_register='Too short password',
                                       login_register='')
        elif request.form['submit'] == 'Login':
            return 'Logging in'
    else:
        return render_template('register.html',
                               regform=regform,
                               loginform=loginform,
                               message_register='',
                               login_register='')


@app.route('/registration_process', methods=['POST'])
def registration_process():
    return 'Registration is successful'
"""

"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)
"""