import datetime

import pytz
from django.conf import settings
from django.core.mail import send_mail
from eMenu.celery import app

from .models import Meal, User


def objects_to_string(objects):
    list_of_dict = list(objects.values())
    return "\n".join(list(map(str, list_of_dict)))


@app.task
def send_email_rapport():
    now = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    one_day = datetime.timedelta(days=1)
    yesterday = now - one_day
    created_yesterday = Meal.objects.filter(create_date__gte=yesterday)
    created_yesterday = objects_to_string(created_yesterday)

    updated_yesterday = Meal.objects.filter(last_update__gte=yesterday, create_date__lt=yesterday)
    updated_yesterday = objects_to_string(updated_yesterday)
    message = "created yesterday: \n" + created_yesterday + "\n updated yesterday: \n" + updated_yesterday
    send_mail(
        subject='That’s your subject',
        message=message,
        from_email='your@djangoapp.com',
        recipient_list=list(User.objects.values_list('email', flat=True)),
        fail_silently=False)
