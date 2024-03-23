from celery import shared_task, Celery

app = Celery('tasks', broker='redis://redis:6379/0')


@shared_task
def task():
    print('task')


@shared_task
def add(x, y):
    return x + y


@shared_task
def multiply(x, y):
    return x * y
