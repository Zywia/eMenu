from django.core.mail import send_mail
from eMenu.celery import app
from .models import Meal
import datetime
import pytz
from django.conf import settings


@app.task
def say(what):
    print(datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)))
    print(Meal.objects.all())
    # send_mail(
    #     subject='That’s your subject',
    #     message='That’s your message body',
    #     from_email='your@djangoapp.com',
    #     recipient_list=['michalgorszczak@gmail.com', 'another@email.com'],
    #     fail_silently=False
    # )
