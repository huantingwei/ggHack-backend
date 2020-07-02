from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

# import django_filters
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions, renderers, mixins, status
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import Http404

from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny


from backend.models import Service, Reservation, FreeSlot
from backend.serializers import UserSerializer, ServiceSerializer, ReservationSerializer, FreeSlotSerializer
from backend.permissions import IsOwner, IsProvider, IsCustomer

import populartimes
API_KEY = 'AIzaSyAH-8I6T-mFTW_e_26ISDs8ChnVCSvKQRs'
# Create your views here.

class ServiceCustomerList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    `list` action for customer(authenticated/non-authenticated) to browse services with search queries
    """
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Filtering against query parameters: name, introduction...
        """
        queryset = Service.objects.all()
        queries = self.request.query_params.get('q', None)
        if queries is not None:
            queryset = queryset.filter(name=queries) # only filtering name now
        return queryset

    @action(methods=['get'], detail=True)
    def get(self, request):
        queryset = self.get_queryset()
        serializer = ServiceSerializer(queryset, many=True)
        return Response(serializer.data)


class ServiceCustomerDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    `retrieve` action for customer to view detail of a service
    """
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ServiceProviderList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    `list`, `create` actions for viewing and creating services.
    Currently allowing any authenticated user to create a service(to become a service provider)
    """
    serializer_class = ServiceSerializer

    def get_queryset(self):
        owner = self.request.user
        return Service.objects.filter(owner=owner)

    @action(methods=['get'], detail=True)
    def get(self, request):
        queryset = self.get_queryset()
        serializer = ServiceSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # TODO: 
    # get_popular_times for PopularTimes
    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        # serializer.data['popularTimes'] = get_popular_times(self, serializer.data['placeId'])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_popular_times(self, place_id):
        popular_times = populartimes.get_id(API_KEY, place_id)
        

class ServiceProviderDetail(mixins.RetrieveModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.DestroyModelMixin, 
                        generics.GenericAPIView):
    """
    `retrieve`, `update`, `destroy` actions for service owner(provider) to configure the services
    """
    permission_classes = [IsOwner]
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    

    @action(methods=['get'], detail=True)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['delete'], detail=True)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    @action(methods=['put'], detail=True)
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ReservationCustomerList(mixins.ListModelMixin, 
                            mixins.CreateModelMixin, 
                            generics.GenericAPIView):
    """
    `list`, `create`, actions for reservation management of customer
    Only the 'reserver' of the reservation is permitted
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        """
        This view should return a list of all the reservations
        for the currently authenticated user.
        """
        customer = self.request.user
        return Reservation.objects.filter(customer=customer)

    @action(methods=['get'], detail=True)
    def get(self, request):
        queryset = self.get_queryset()
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # TODO: need to 
    # (1) check availability (> maxCapacity?)
    # (2) update capacity table

    def create(self, request, *args, **kwargs):
        data = self._preprocess(request)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _preprocess(self, request):
        data = request.data.dict()
        service_name = data['service']
        data['customer'] = request.user.id
        service = Service.objects.get(name=service_name)
        data['serviceOwner'] = service.owner.id
        data['service'] = service.id
        
        return data


class ReservationCustomerDetail(mixins.RetrieveModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.DestroyModelMixin, 
                        generics.GenericAPIView):
    """
    `retrieve`, `update`, `destroy` actions for service owner(provider) to configure the services
    """
    permission_classes = [IsCustomer]
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    
    def get_queryset(self):
        """
        This view should return a list of all the reservations
        for the currently authenticated user.
        """
        customer = self.request.user
        return Reservation.objects.filter(customer=customer)
        
    @action(methods=['get'], detail=True)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['delete'], detail=True)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    @action(methods=['put'], detail=True)
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ReservationProviderList(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsProvider]

    def get_queryset(self):
        """
        This view should return a list of all the reservations
        for the currently authenticated user.
        """
        serviceOwner = self.request.user
        return Reservation.objects.filter(serviceOwner=serviceOwner)
    
    @action(methods=['get'], detail=True)
    def get(self, request):
        queryset = self.get_queryset()
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)


class ReservationProviderDetail(mixins.RetrieveModelMixin, 
                        mixins.UpdateModelMixin, 
                        generics.GenericAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsProvider]

    def get_queryset(self):
        serviceOwner = self.request.user
        return Reservation.objects.filter(serviceOwner=serviceOwner)
    
    
    @action(methods=['get'], detail=True)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    @action(methods=['put'], detail=True)
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    