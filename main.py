from threading import Thread
from uuid import uuid4

from flask import Flask
from flask import request
from flask import render_template

from factorial import factorial
from compute_pi import compute_pi
from compute_e import compute_e


app = Flask(__name__)

function_registry = {
    'factorial': factorial,
    'pi': compute_pi,
    'e': compute_e
}

results = {}

tables = []
ID = 0


@app.route('/', method=['GET'])
def index():
    return render_template('index.html')


@app.route('/schedule_calculation', method=['POST'])
def schedule_calculation():
    assert request.method == 'POST'

    # get parameters

    func_name = request.form['func_name']
    argument = request.form['argument']
    accuracy = request.form['accuracy']

    try:
        func = function_registry[func_name]
    except KeyError:
        raise
        # TODO (dmitry):  return message that we don't have such function

    uuid = uuid4()

    # create thread
    thread = Thread(target=func, args=(argument, accuracy, uuid, results))

    results[uuid] = {
        'func_name': func_name,
        'argument': argument,
        'requested_accuracy': accuracy,
        'result': 'IN PROGRESS',
        'value': None,
        'accuracy_achieved': None
    }

    # start thread execution
    thread.start()



@app.route('/results', method=['GET'])
def results():

    return render_template('results.html', results=results)



@app.route("/", methods=["POST", "GET"])
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

            [out_val, accuracy] = registry[func_name](inp_val, n_digits)
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