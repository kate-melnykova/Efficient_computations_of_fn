from time import time

from flask import Blueprint
from flask import flash
from flask import url_for
from flask import redirect
from flask import request
from flask import render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
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
redis_connection_user = Redis(host='redis', port=6379, db=1)


@login_manager.user_loader
def user_loader(username):
    user_db = redis_connection_user.get(username)
    if user_db is not None:
        user_db = json.loads(user_db)
        user = User.convert_user_db_to_user(user_db)
        return user
    else:
        return None


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
    print(f'Current user on index page {current_user}')
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
        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
        
        
        
        # handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
"""