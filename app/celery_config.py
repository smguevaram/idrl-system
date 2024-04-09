from celery import Celery

def make_celery():
    celery = Celery('app', backend='redis://redis:6379/0', broker='redis://redis:6379/0')
    return celery
