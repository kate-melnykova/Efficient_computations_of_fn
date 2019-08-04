from time import time
from uuid import uuid4

from celery import Celery
from flask import Flask
from flask import url_for
from flask import redirect
from flask import request
from flask import render_template
import json
from redis import Redis

from login_form import RegistrationForm
from sci_funcs.tasks import args_to_function
from sci_funcs.function_registry import function_registry


app = Flask(__name__)
app.config['broker_url'] = 'amqp://rabbitmq:5672//'
app.config['result_backend'] = 'redis://redis:6379'
app.config['imports'] = ['sci_funcs.tasks']

celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)
celery.set_default()


@app.route('/', methods=['GET'])
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

    r = Redis(host='redis',
              port=6379,
              db=0)
    message = json.dumps({"status": "PENDING",
                          "result":  arguments,
                          "task_id": async_result.task_id
                          })
    r.set(str.encode('celery-task-meta-' + async_result.task_id),
          message)
    return redirect(url_for('view_results'))


@app.route('/view_results', methods=['GET'])
def view_results():
    r = Redis(host='redis',
              port=6379,
              db=0)
    results_temp = {}
    for key in r.keys('*'):
        result = json.loads(r.get(key))
        task_id = result['task_id']
        result = result['result']
        results_temp[task_id] = result

    return render_template('view_results.html',
                           results=results_temp)


# @app.route('/view_result<uuid>', methods=['GET'])
@app.route('/result', methods=['GET'])
def view_specific_results():
    task_id = str(request.args.get('task_id', ''))
    r = Redis(host='redis',
              port=6379,
              db=0)
    key = str.encode('celery-task-meta-' + task_id)
    try:
        result = json.loads(r.get(key))
    except:
        return 'Task not found'

    result = result['result']
    return render_template(f'{ result["func_name"] }.html',
                           result=result)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['confirm']
        return 'Registration is successful'
    else:
        return render_template('register.html', form=form)
