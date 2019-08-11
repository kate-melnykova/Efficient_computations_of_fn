from celery import Celery
from flask import Flask
from flask import url_for
from flask import redirect
from flask import request
from flask import render_template
import flask_login
import json
from redis import Redis


def factory_app():
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config['broker_url'] = 'amqp://rabbitmq:5672//'
    app.config['result_backend'] = 'redis://redis:6379'
    app.config['imports'] = ['sci_funcs.tasks']
    app.secret_key = 'super secret string'  # Change this!

    celery = Celery(app.name, broker=app.config['broker_url'])
    celery.conf.update(app.config)
    celery.set_default()

    redis_connection = Redis(host='redis',
                             port=6379,
                             db=0)
    return app, celery, redis_connection