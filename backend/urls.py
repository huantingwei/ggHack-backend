from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'services', views.ServiceViewSet)
router.register(r'reservations', views.ReservationViewSet)
router.register(r'create_user', views.CreateUserView)

# The API urls are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]