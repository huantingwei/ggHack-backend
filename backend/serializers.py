# from django.contrib.auth.models import User
from rest_framework import serializers

from backend.models import User, Service, Reservation

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

    # def create(self, validated_data):
    #     user = User(**validated_data)
    #     # Hash the user's password.
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user


class ServiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'address', 'introduction', 'type', 'longitude', 'latitude', 'rating']

class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'service', 'startTime', 'endTime']