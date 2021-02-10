from time import time

from flask import Blueprint
from flask import flash
from flask import url_for
from flask import redirect
from flask import request
from flask import render_template
import json

from compare_time import get_time_consumption
from factory_app import factory_app
from sci_funcs import compute_pi, compute_e, factorial

app = factory_app()


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/pi')
def pi():
    try:
        accuracy = int(request.args.get('accuracy', 3))
    except ValueError:
        flash('Incorrect number of digits, must be integers')
        return redirect(url_for('index'))

    n_runs = 10000
    # run it 10000 times
    mean, std = get_time_consumption(lambda: compute_pi.compute_pi(accuracy),
                                     n_runs=n_runs)
    return render_template('pi.html',
                           accuracy=accuracy,
                           mean=mean,
                           std=std,
                           n_runs=n_runs)


@app.route('/exponent')
def exponent():
    accuracy = request.args.get('accuracy', 3)
    return render_template('exponent.html',
                           accuracy=accuracy)


@app.route('/factorial')
def factorial():
    argument = request.args.get('argument', 1000)
    return render_template('factorial.html',
                           argument=argument)


