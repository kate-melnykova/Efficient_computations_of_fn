from time import time
from threading import Thread
import os
from uuid import uuid4

from celery import Celery
from celery import shared_task
from flask import Flask
from flask import url_for
from flask import redirect
from flask import request
from flask import render_template
from flask import render_template_string
import json
from redis import Redis

#from app import factorial
from factorial import factorial
from compute_pi import compute_pi
from compute_e import compute_e

class Args:
    def __init__(self):
        self.argument = 3
        self.time_limit = 3
        self.accuracy = 3


app = Flask(__name__)
app.config['broker_url'] = 'amqp://rabbitmq:5672//'
app.config['result_backend'] = 'redis://redis:6379'

celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)


function_registry = {
    'factorial': [factorial, 'argument', 'time_limit', 'accuracy'],
    'pi': [compute_pi, 'time_limit', 'accuracy'],
    'e': [compute_e, 'time_limit', 'accuracy']
}

results = {}
args = Args()
tables = []
ID = 0


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', args=args)


@celery.task
def function_implementation(func_name, uuid, results, arg_names):
    print("We are here")
    func = function_registry[func_name][0]
    func(uuid, results, arg_names)
    return results[uuid]


@app.route('/schedule_calculation', methods=['POST'])
def schedule_calculation():
    global results
    assert request.method == 'POST'

    # get parameters
    func_name = request.form['func_name']
    try:
        func = function_registry[func_name][0]

    except KeyError:
        raise
        # TODO (dmitry):  return message that we don't have such function

    uuid = str(uuid4())

    results[uuid] = dict()
    results[uuid]['func_name'] = str(func.__name__)
    results[uuid]['status'] = 'IN PROGRESS'
    results[uuid]['start_time'] = time()

    # remove the oldest computation if needed
    if len(results) > 10:
        oldest_uuid = min(([results[uuid_]['start_time'], uuid_] for uuid_ in results.keys()))
        oldest_uuid = oldest_uuid[1]
        del results[oldest_uuid]

    # read all arguments and add it to results
    for item in function_registry[func_name][1:]:
        results[uuid][item] = request.form[item]

    function_implementation.delay(func_name,
                                  uuid,
                                  results,
                                  function_registry[func_name][1:])

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