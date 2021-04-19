import datetime

import pytz
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Meal, Card


@receiver(pre_save, sender=Meal)
def meal_callback(sender, instance, raw, using, update_fields, **kwargs):
    instance.last_update = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))


@receiver(pre_save, sender=Card)
def card_callback(sender, instance, raw, using, update_fields, **kwargs):
    instance.last_update = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
