from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
#router.register(r'capacityTable', views.CapacityTableViewSet)

# The API urls are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('customer/services', views.ServiceCustomerList.as_view()),
    path('customer/services/<int:pk>', views.ServiceCustomerDetail.as_view()),
    path('customer/reservations', views.ReservationCustomerList.as_view()),
    path('customer/reservations/<int:pk>', views.ReservationCustomerDetail.as_view()),
    path('provider/services', views.ServiceProviderList.as_view()),
    path('provider/services/<int:pk>', views.ServiceProviderDetail.as_view()),
    path('provider/reservations', views.ReservationProviderList.as_view()),
    path('provider/reservations/<int:pk>', views.ReservationProviderDetail.as_view()),
]
