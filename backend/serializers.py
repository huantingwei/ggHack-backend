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


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Service
        fields = ['url', 'id', 'name', 'address', 'introduction']

class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['url', 'id', 'user', 'service', 'startTime', 'endTime']