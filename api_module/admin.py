from django.contrib import admin
from . import models

admin.site.register(models.Booking)
admin.site.register(models.Vehicle)
admin.site.register(models.VehicleType)
admin.site.register(models.Route)
admin.site.register(models.ActiveVehicle)
admin.site.register(models.Seat)