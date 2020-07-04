from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import F
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver 
from django.core.exceptions import ValidationError

import populartimes
API_KEY = 'AIzaSyAH-8I6T-mFTW_e_26ISDs8ChnVCSvKQRs'

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
    owner = models.ForeignKey(
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
    rating = models.FloatField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    maxCapacity = models.IntegerField(default=10) 
    startTime = models.IntegerField() # TimeField()
    closeTime = models.IntegerField() # TimeField()

    placeId = models.TextField()
    freeSlots = ArrayField(
        ArrayField(models.IntegerField(blank=True, null=True)),
        blank=True, null=True,
    )
    popularTimes = ArrayField(
        ArrayField(models.IntegerField(blank=True, null=True)),
        blank=True, null=True,
    )
    
    def __str__(self):
        return self.name


def init_freeslots(instance):
    openningHours = instance.closeTime - instance.startTime
    mon = [instance.maxCapacity for i in range(openningHours)]
    tue = [instance.maxCapacity for i in range(openningHours)]
    wed = [instance.maxCapacity for i in range(openningHours)]
    thu = [instance.maxCapacity for i in range(openningHours)]
    fri = [instance.maxCapacity for i in range(openningHours)]
    sat = [instance.maxCapacity for i in range(openningHours)]
    sun = [instance.maxCapacity for i in range(openningHours)]
    return [mon, tue, wed, thu, fri, sat, sun]

def get_place_detail(instance):
    try:
        place_detail = populartimes.get_id(API_KEY, instance.placeId)
    except:
        return None
    
    popular_times = get_popular_times(place_detail)
    lat, lon = get_lat_lon(place_detail)
    rating = get_rating(place_detail)

    return popular_times, lat, lon, rating

def get_rating(place_detail):
    if 'rating' in place_detail.keys():
        return place_detail['rating']
    else:
        return -1

def get_lat_lon(place_detail):
    if 'coordinates' in place_detail.keys():
        lat = place_detail['coordinates']['lat']
        lon = place_detail['coordinates']['lng']
    else:
        lat = 0
        long = 0
    return lat, lon

def get_popular_times(place_detail):

    data = []
    if 'populartimes' in place_detail.keys():
        popular_times = place_detail['populartimes']
        for d in popular_times:
            data.append(d['data'])
        
        assert len(data) == 7 and len(data[0]) == 24, 'error in get_popular_times' 
    else:
        data = [[] for _ in range(7)]
        
    return data

@receiver(post_save, sender = Service, dispatch_uid='init service')
def init_service(sender, instance, created, **kwargs):
    if created:
        instance.freeSlots = init_freeslots(instance)
        place_detail = list(get_place_detail(instance))
        if place_detail[0] is not None:
            instance.popularTimes = place_detail[0]
            instance.latitude = place_detail[1]
            instance.longitude = place_detail[2]
            instance.rating = place_detail[3]

        instance.save()
#post_save.connect(init_service, sender=Service)


class Reservation(models.Model):
    customer = models.ForeignKey(
        User,
        related_name = 'reserved_by',
        on_delete = models.CASCADE
    )
    service = models.ForeignKey(
        Service,
        on_delete = models.CASCADE
    )
    serviceOwner = models.ForeignKey(
        User,
        related_name = 'of_service_owned_by',
        on_delete = models.CASCADE
    )
    WEEK_DAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    )
    bookDate = models.IntegerField(
        choices=WEEK_DAYS,
        default='Monday'
    )
    bookTime = models.IntegerField()
    numPeople = models.IntegerField()

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
        return self.customer.username + ' : ' + self.service.name

    # validation
    def clean(self):
        service = self.service
        if not (self.bookTime >= service.startTime):
            raise ValidationError('bookTime must be >= startTime')

        if not (service.closeTime > self.bookTime):
            raise ValidationError('bookTime must be < closeTime')

        date = self.bookDate
        time = self.bookTime - service.startTime

        if not (self.numPeople <= service.freeSlots[date][time]):
            raise ValidationError('There is no enough free slots!')
        
        if not (self.numPeople >= 1):
            raise ValidationError('numPeople should be at least 1!')

        


@receiver(post_save, sender = Reservation, dispatch_uid='reservation update freeslots')
def reservation_update_freeslots(sender, instance, created, **kwargs):
    if instance and created:
        date = int(instance.bookDate)
        time = instance.bookTime - instance.service.startTime
        instance.service.freeSlots[date][time] -= instance.numPeople
        instance.service.save()
      

@receiver(post_delete, sender=Reservation)
def delete_reservation(sender, instance, *args, **kwargs):
    date = int(instance.bookDate)
    time = instance.bookTime - instance.service.startTime
    instance.service.freeSlots[date][time] += instance.numPeople
    instance.service.save()


