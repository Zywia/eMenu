# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Card(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
