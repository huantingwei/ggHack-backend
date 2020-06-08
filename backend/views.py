from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import viewsets, generics, permissions, renderers
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from backend.models import Service, Reservation
from backend.serializers import ServiceSerializer, ReservationSerializer #, UserSerializer
from backend.permissions import IsOwnerOrReadOnly

# Create your views here.

class ServiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]#, IsOwnerOrReadOnly]

class ReservationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]#, IsOwnerOrReadOnly]