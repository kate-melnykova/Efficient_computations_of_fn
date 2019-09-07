from celery import Celery
from flask import Flask, render_template


def page_not_found(e):
    return render_template('404.html'), 404


def forbidden(e):
    return render_template('403.html'), 403


def unautharized(e):
    return render_template('401.html'), 401


def factory_app():
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.secret_key = '1e9424b4-737b-4f49-91fa-cdb6290984e7'
    app.config.from_object('config')
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(401, unautharized)

    celery = Celery(app.name)
    celery.set_default()
    celery.conf.update(app.config)
    celery.config_from_object('celeryconf')
    return app, celery