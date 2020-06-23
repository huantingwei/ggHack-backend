from django.contrib import admin

from backend.models import Service, Reservation, CapacityTable, User

# Register your models here.
admin.site.register(Service)
admin.site.register(Reservation)
admin.site.register(CapacityTable)
admin.site.register(User)