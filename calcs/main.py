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
    return render_template('pi.html')

@app.route('/exponent')
def exponent():
    return render_template('exponent.html')

@app.route('/factorial')
def factorial():
    return render_template('factorial.html')


