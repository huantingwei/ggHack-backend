# from django.contrib.auth.models import User
from rest_framework import serializers

from backend.models import User, Service, Reservation

class UserSerializer(serializers.ModelSerializer):

    reservations = serializers.PrimaryKeyRelatedField(many=True, queryset=Reservation.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'reservations']


class ServiceSerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Service
        fields = ['id', 'owner', 'name', 'address', 'introduction', 'type', 'longitude', 'latitude', 'rating', 'image']


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'provider', 'startTime', 'endTime']
