''' Admin module of api '''
from django.contrib import admin
from .models import Layout, Seat, Vehicle, VehicleType, Booking, Route, ScheduledVehicle

admin.site.register(Layout)
admin.site.register(Seat)
admin.site.register(VehicleType)
admin.site.register(Route)
admin.site.register(Vehicle)
admin.site.register(ScheduledVehicle)
admin.site.register(Booking)
