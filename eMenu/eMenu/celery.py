import os

from celery import Celery

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eMenu.settings')

app = Celery('eMenu')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'test': {
        'task': 'menuCard.tasks.send_email_rapport',
        'schedule': crontab(hour=10, minute=0, day_of_week='*'),
        'args': [],
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
