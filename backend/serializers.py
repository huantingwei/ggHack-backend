# from django.contrib.auth.models import User
from rest_framework import serializers
from django.forms.models import model_to_dict

from backend.models import User, Service, Reservation,  PopularTimes


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ServiceSerializer(serializers.ModelSerializer):
    
    owner = serializers.StringRelatedField()

    class Meta:
        model = Service
        fields = ['id', 'owner', 'name', 'address', 'introduction', 'type', 
                'longitude', 'latitude', 'rating', 'image', 
                'maxCapacity', 'placeId', 'freeSlot', 'popularTimes']
    
    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        print(ret)
        return ret

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            ret['freeSlot'] = FreeSlot.objects.get(pk=ret['freeSlot'])
            ret['popularTimes'] = PopularTimes.objects.get(pk=ret['popularTimes'])
        except:
            return ret
        return ret

class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'service', 'serviceOwner', 'bookDate','bookTime', 'numPeople',  'status']

    def validate(self, data):
        """
        Check that startTime is before endTime.
        """
        if data['startTime'] > data['endTime']:
            raise serializers.ValidationError("startTime must occur before endTime")
        return data

    def to_representation(self, instance):
        return {
            'id': instance.id, 
            'customer': instance.customer.username, 
            'service': model_to_dict(Service.objects.get(name=instance.service.name)),
            'serviceOwner': instance.serviceOwner.username, 
            #'startTime': instance.startTime,
            #'endTime': instance.endTime, 
            'bookDate': instance.bookDate,
            'bookTime': instance.bookTime,
            'numPeople': instance.numPeople,
            'status': instance.status
        }
