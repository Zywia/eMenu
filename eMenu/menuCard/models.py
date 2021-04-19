# Create your models here.
from concurrency.fields import IntegerVersionField
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Meal(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    time_to_prepare = models.TimeField()
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)
    version = IntegerVersionField()


class Card(models.Model):
    title = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)
    meal = models.ManyToManyField(Meal)
    version = IntegerVersionField()

    def __str__(self):
        return self.title
