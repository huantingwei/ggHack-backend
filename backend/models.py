from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=False,
        null=False,
    )
    username = models.CharField(max_length=255, unique=False)
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

class Service(models.Model):
    CLINIC = 'CL' 
    HAIRSALON = 'HS'
    RESTAURANT = 'RE'
    SHOP = 'SH'
    SERVICE_TYPE = (
        (CLINIC, 'Clinic'),
        (HAIRSALON, 'Hair Salon'),
        (RESTAURANT, 'Restaurant'),
        (SHOP, 'Shop')
    )

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User,
        related_name = 'ownedServices',
        on_delete = models.CASCADE
    )
    address = models.TextField()
    introduction = models.TextField()
    type = models.CharField(
        max_length=2,
        choices=SERVICE_TYPE,
        default=SHOP,
    )
    longitude = models.FloatField()
    latitude = models.FloatField()
    rating = models.FloatField()
    image = models.URLField(default='./images/default.jpg')
    # discard `reservations` field because it could be queried from Reservation

    # how to represent capacity and popularTimes? 

class Reservation(models.Model):
    customer = models.ForeignKey(
        User,
        related_name = 'reservations',
        on_delete = models.CASCADE
    )
    provider = models.ForeignKey(
        Service,
        related_name = 'reservations',
        on_delete = models.CASCADE
    )
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

    COMPLETED = 'CP'
    PENDING = 'PD'
    MISSED = 'MS'
    STATUS = (
        (COMPLETED, 'completed'),
        (PENDING, 'pending'),
        (MISSED, 'missed')
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=PENDING
    )

