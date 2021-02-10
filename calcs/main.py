from time import time

from flask import Blueprint
from flask import flash
from flask import url_for
from flask import redirect
from flask import request
from flask import render_template
import json

from factory_app import factory_app

app = factory_app()


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/pi')
def pi():
    accuracy = request.args.get('accuracy', 3)
    # run it 1000 times
    direct_times = ...
    return render_template('pi.html',
                           accuracy=accuracy)

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


