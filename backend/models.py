from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models
from django_mysql.models import ListCharField

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=False,
        null=False,
    )
    username = models.CharField(max_length=50, unique=True,blank=False,null=False)
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.username


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
    image = models.URLField()

    # how to represent capacity and popularTimes? 
    maxCapacity = models.IntegerField(default=10)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    service = models.ForeignKey(
        Service,
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

    def __str__(self):
        return self.user.username + ' ' + self.service.name

class CapacityTable(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete = models.CASCADE
    )
    # Suppose opening time: 12:00 - 20:00 
    mon = ListCharField(
        base_field = models.CharField(max_length=5),
        size=8,
        max_length=(8 * 6)  # 6 * 10 character nominals, plus commas
    )
    tue = ListCharField(
        base_field = models.CharField(max_length=5),
        size=8,
        max_length=(8 * 6)  # 6 * 10 character nominals, plus commas
    )
    wed = ListCharField(
        base_field = models.CharField(max_length=5),
        size=8,
        max_length=(8 * 6)  # 6 * 10 character nominals, plus commas
    )
    thu = ListCharField(
        base_field = models.CharField(max_length=5),
        size=8,
        max_length=(8 * 6)  # 6 * 10 character nominals, plus commas
    )
    fri = ListCharField(
        base_field = models.CharField(max_length=5),
        size=8,
        max_length=(8 * 6)  # 6 * 10 character nominals, plus commas
    )
    sat = ListCharField(
        base_field = models.CharField(max_length=5),
        size=8,
        max_length=(8 * 6)  # 6 * 10 character nominals, plus commas
    )
    sun = ListCharField(
        base_field = models.CharField(max_length=5),
        size=8,
        max_length=(8 * 6)  # 6 * 10 character nominals, plus commas
    )

