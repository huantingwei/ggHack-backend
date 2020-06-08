from django.contrib.auth.models import User
from rest_framework import serializers

from backend.models import Service, Reservation

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Service
        fields = ['url', 'id', 'name', 'address', 'description']

class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['url', 'id', 'user', 'service', 'start_time', 'end_time']