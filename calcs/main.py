from time import time

from flask import Blueprint
from flask import flash
from flask import url_for
from flask import redirect
from flask import request
from flask import render_template
from flask_login import LoginManager, UserMixin, login_required,\
    login_user, logout_user, current_user
import json
from redis import Redis

from factory_app import factory_app
from redispy import get_connection
from views.auth import User
from views.auth.login_form import auth
from sci_funcs.tasks import args_to_function
from sci_funcs.function_registry import function_registry

app, celery = factory_app()

######
# LoginManager setup
######
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(username):
    user_db = get_connection(db=app.config['USER_DB']).get(username)
    if user_db is not None:
        return User.deserialize(user_db)
    else:
        return None


app.register_blueprint(auth)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    print(f'Current user on index page {current_user}')
    return render_template('index.html')


@app.route('/schedule_calculation', methods=['POST'])
def schedule_calculation():
    assert request.method == 'POST'

    func_name = request.form['func_name']
    if func_name in function_registry:
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
        get_connection(db=app.config['CALCS_DB']).set(f'celery-task-meta-{async_result.task_id}',
                                                      message)
        return redirect(url_for('view_results'))
    else:
        assert func_name == 'expression'
        expression = request.form.expression
        flash(f'Submitted {expression}')
        return redirect(url_for('index'))


@app.route('/view_results', methods=['GET'])
def view_results():
    results_temp = {}
    connection = get_connection(db=app.config['CALCS_DB'])
    for key in connection.keys('*'):
        result = json.loads(connection.get(key))
        print(result)
        task_id = result['task_id']
        result = result['result']
        results_temp[task_id] = result

    return render_template('view_results.html',
                           results=results_temp)


@app.route('/result', methods=['GET'])
@login_required
def view_specific_results():
    task_id = str(request.args.get('task_id', ''))
    key = str.encode(f'celery-task-meta-{task_id}')
    try:
        result = json.loads(get_connection(db=app.config['CALCS_DB']).get(key))
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