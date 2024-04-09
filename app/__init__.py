from flask import Flask
from .celery_config import make_celery
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    register_routes(app)

    app.config['UPLOAD_FOLDER'] = '/app/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

    celery = make_celery()
    celery.conf.update(app.config)
    app.celery = celery

    return app
