from time import time
from threading import Thread
from uuid import uuid4

from celery import Celery
from celery import shared_task
from flask import Flask
from flask import url_for
from flask import redirect
from flask import request
from flask import render_template
from flask import render_template_string

from .factorial import factorial
from .compute_pi import compute_pi
from .compute_e import compute_e


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

"""
@celery.task(shared=True)
def addition(a=2, b=3):
    time.sleep(1)
    num = a + b
    print(f"Ended shared_task, answer = {num}")
    return num
"""


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
    print(str(uuid))

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

    # create thread
    thread = Thread(target=func, args=(uuid, results, function_registry[func_name][1:]))

    # start thread execution
    thread.start()

    # return render_template('view_results.html', results=results)
    # return render_template('schedule_calculation.html')
    return redirect(url_for('view_results'))


@app.route('/view_results', methods=['GET'])
def view_results():
    return render_template('view_results.html', results=results)


# @app.route('/view_result<uuid>', methods=['GET'])
@app.route('/result', methods=['GET'])
def view_specific_results():
    uuid = str(request.args.get('uuid', ''))
    return render_template(f'{ results[uuid]["func_name"] }.html', result=results[uuid])
    # return render_template_string(f'Shows result for {uuid}')


@app.route("/old_version", methods=["POST", "GET"])
def implementation():
    global ID, tables
    if request.method == 'POST':
        if request.form['submit_button'] == 'submit':
            func_name = request.form["func_name"]
            inp_val = int(request.form['inp'])
            n_digits = int(request.form['n_digits'])

            tables.append([ID, func_name, inp_val, n_digits, "Computing...", "", ""])
            if len(tables) > 10:
                del tables[0]
            id_loc = ID
            ID += 1

            [out_val, accuracy] = function_registry[func_name](inp_val, n_digits)
            out_val = str(out_val)
            tables[-1][4] = "yes"

            # crop number if needed
            if len(out_val) > n_digits:
                if "." not in out_val[:n_digits]:
                    out_val = out_val[:n_digits+1] + "E+" + str(len(out_val)-n_digits)
                else:
                    out_val = out_val[:n_digits + 2]

            idx = 70
            while idx < len(out_val):
                out_val = out_val[:idx] + '\n ...' + out_val[idx:]
                idx += 70

            #find row with ID = id_loc
            for i in range(len(tables)):
                found = tables[i][0] == id_loc
                if found:
                    break
            if found:
                tables[i][5] = out_val
                tables[i][6] = accuracy

            return render_template('index.html', tables=tables,
                                   inp=inp_val, func_name=func_name, out_val=out_val, acc=accuracy)
        else:
            # we need to figure out which form is submitted
            id_view = request.form['submit_button']
            for i in range(len(tables)):
                found = tables[i][0] == int(id_view)
                if found:
                    break
            if found:
                return render_template('index.html', tables=tables,
                                       inp=tables[i][2], func_name=tables[i][1],
                                       out_val=tables[i][5], acc=tables[i][6])
            else:
                return render_template('index.html', tables=tables, inp=None, func_name=None,
                                       out_val=None, acc=None)
    else:
        return render_template('index.html', tables=tables,
                               inp=None, func_name=None, out_val=None, acc=None)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)