# from django.contrib.auth.models import User
from rest_framework import serializers
from django.forms.models import model_to_dict
from backend.models import User, Service, Reservation, CapacityTable


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ServiceSerializer(serializers.ModelSerializer):
    
    owner = serializers.StringRelatedField()

    class Meta:
        model = Service
        fields = ['id', 'owner', 'name', 'address', 'introduction', 'type', 'longitude', 'latitude', 'rating', 'image', 'maxCapacity']


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'service', 'serviceOwner', 'startTime', 'endTime', 'status']

    def to_representation(self, instance):
        return {
            'id': instance.id, 
            'customer': instance.customer.username, 
            'service': model_to_dict(Service.objects.get(name=instance.service.name)),
            'serviceOwner': instance.serviceOwner.username, 
            'startTime': instance.startTime,
            'endTime': instance.endTime, 
            'status': instance.status
        }

class CapacitySerializer(serializers.ModelSerializer):

    class Meta:
        model = CapacityTable
        fields = '__all__'
