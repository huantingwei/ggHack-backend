from django.contrib.auth.models import AbstractUser
from django.db import models
#from django_mysql.models import ListCharField
from django.contrib.postgres.fields import ArrayField
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
    REQUIRED_FIELDS = ['email'] 
 
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
    owner = models.OneToOneField(
        User,
        related_name = 'owned_by',
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
    image = models.URLField()

    # how to represent capacity and popularTimes? 
    maxCapacity = models.IntegerField(default=10)

    def __str__(self):
        service = {
            'name': self.name,
            'owner': self.owner,
            'address': self.address,
            'introduction': self.introduction,
            'type': self.type,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'rating': self.rating,
            'image': self.image,
            'maxCapacity': self.maxCapacity
        }
        return str(service)
      

class Reservation(models.Model):
    customer = models.ForeignKey(
        User,
        related_name = 'reserved_by',
        on_delete = models.CASCADE
    )
    service = models.ForeignKey(
        Service,
        related_name = 'of_service',
        on_delete = models.CASCADE
    )
    serviceOwner = models.ForeignKey(
        User,
        related_name = 'of_service_owned_by',
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
        return self.customer.username + ' : ' + self.service.name + ' : ' + self.serviceOwner.username

class CapacityTable(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete = models.CASCADE
    )
    # Suppose opening time: 12:00 - 20:00 
    mon = ArrayField(models.IntegerField())
    tue = ArrayField(models.IntegerField())
    wed = ArrayField(models.IntegerField())
    thu = ArrayField(models.IntegerField())
    fri = ArrayField(models.IntegerField())
    sat = ArrayField(models.IntegerField())
    sun = ArrayField(models.IntegerField())

