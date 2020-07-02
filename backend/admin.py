from django.contrib import admin

from backend.models import Service, Reservation, FreeSlot, User

# Register your models here.
admin.site.register(Service)
admin.site.register(Reservation)
admin.site.register(FreeSlot)
admin.site.register(User)