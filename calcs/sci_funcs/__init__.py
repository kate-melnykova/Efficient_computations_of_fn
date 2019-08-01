"""
from celery import Celery

def create_celery(app):
    celery = Celery(app.name, broker=app.config['broker_url'])
    celery.conf.update(app.config)
    return celery
"""