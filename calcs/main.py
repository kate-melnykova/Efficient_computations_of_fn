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

from factorial import factorial
from compute_pi import compute_pi
from compute_e import compute_e

from sci_funcs.tasks import functio


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

    function_registry = {
        'factorial': [factorial, 'argument', 'time_limit', 'accuracy'],
        'pi': [compute_pi, 'time_limit', 'accuracy'],
        'e': [compute_e, 'time_limit', 'accuracy']
    }

    # get parameters
    func_name = request.form['func_name']
    try:
        func = function_registry[func_name][0]

    except KeyError:
        raise
        # TODO (dmitry):  return message that we don't have such function

    uuid = str(uuid4())

    arguments = dict()
    # TODO: fix
    arguments['func_name'] = str(func.__name__)
    arguments['status'] = 'IN PROGRESS'
    arguments['start_time'] = time()

    # read all arguments and add it to results
    for item in function_registry[func_name][1:]:
        arguments[item] = request.form[item]

    # get task identifier
    async_result = functio.delay(func_name, arguments, function_registry[func_name][1:])
    print('Async_result', async_result)
    print('Type of task_id', async_result.task_id, type(async_result.task_id))
    r = Redis(host='redis',
              port=6379,
              db=0)
    message = json.dumps(arguments)
    # r.set(b''.join(['celery-task-meta-',async_result.task_id]), json.dumps(''))
    # TODO: check syntax -- serialize the line using json.dumps
    return redirect(url_for('view_results'))


@app.route('/view_results', methods=['GET'])
def view_results():
    r = Redis(host='redis',
              port=6379,
              db=0)
    results_temp = {}
    for key in r.keys('*'):
        print('Pickled', r.get(key))
        try:
            result = json.loads(r.get(key))
            print('Unpickled', result)
            # if 'result' in result:
            # celery worker result
            task_id = result['task_id']
            result = result['result']
            results_temp[task_id] = result
        except:
            # in progress
            # results_temp[task_id] = {}
            # TODO: status is Pending
            pass

    return render_template('view_results.html',
                           results=results_temp)


# @app.route('/view_result<uuid>', methods=['GET'])
@app.route('/result', methods=['GET'])
def view_specific_results():
    task_id = str(request.args.get('task_id', ''))
    r = Redis(host='redis',
              port=6379,
              db=0)
    for key in r.keys('*'):
        result = json.loads(r.get(key))
        if task_id == result['task_id']:
            result = result['result']
            return render_template(f'{ result["func_name"] }.html',
                                   result=result)
    return "Task not found"


    """
    # create thread
    thread = Thread(target=func, args=(uuid, results, function_registry[func_name][1:]))

    # start thread execution
    thread.start()
    """

    """
    curl -X POST -d 'func_name=factorial' -d 'argument=3' -d 'time_limit=1' -d 'accuracy=10' http://0.0.0.0:5000/schedule_calculation --verbose
    """