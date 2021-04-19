import os

from celery import Celery
# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eMenu.settings')

app = Celery('eMenu')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'test': {
        'task': 'menuCard.tasks.say',
        'schedule': crontab(hour='*', minute='*', day_of_week='*'),
        'args': ['hello world!!!'],
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
