from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from django.shortcuts import render
from django.contrib.auth import get_user_model
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics, permissions, renderers, mixins, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from backend.models import Service, Reservation, CapacityTable
from backend.serializers import UserSerializer, ServiceSerializer, ReservationSerializer, CapacitySerializer
from backend.permissions import IsOwnerOrReadOnly

# Create your views here.

# obsolete if use rest-auth
# class CreateUserView(CreateModelMixin, GenericViewSet):
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = ServiceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Service.objects.all()
    # could change to `def get_queryset(self):` for advanced processing(filtering...)
    # see more details at https://www.django-rest-framework.org/api-guide/generic-views/

class ReservationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = ReservationSerializer
    # permission_classes = IsOwnerOrReadOnly
    queryset = Reservation.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('user',)

class CapacityTableViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = CapacitySerializer
    # permission_classes = IsOwnerOrReadOnly
    queryset = CapacityTable.objects.all()
    
