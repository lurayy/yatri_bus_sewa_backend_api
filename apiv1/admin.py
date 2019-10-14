''' Admin module of api '''
from django.contrib import admin
from .models import LayoutItem, Layout, SeatItem, Seat, VehicleItem, Vehicle, VehicleType, Booking, Route

admin.site.register(Layout)
admin.site.register(LayoutItem)

admin.site.register(Seat)
admin.site.register(VehicleType)
admin.site.register(Route)
admin.site.register(Vehicle)
admin.site.register(VehicleItem)
admin.site.register(Booking)
admin.site.register(SeatItem)
