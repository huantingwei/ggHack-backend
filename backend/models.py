from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# self defined User
# class User(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=100)

# but can actually be replaced by built-in authentication if we don't want customized ones
# from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    location = models.FloatField()
    introduction = models.TextField()
    rating = models.FloatField()

class Reservation(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )
    service = models.OneToOneField(
        Service,
        on_delete = models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


