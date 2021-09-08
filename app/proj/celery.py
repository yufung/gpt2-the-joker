from celery import Celery

app = Celery(
    'proj',
    backend='redis://redis:6379/0',
    broker='redis://redis:6379/0',
    imports=['proj.tasks'])

if __name__ == '__main__':
    app.start()