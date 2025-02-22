''' Module containing the url patterns of api v1 '''

from django.urls import path
from . import views

urlpatterns = [
    path('layouts/', views.layouts, name='layouts'),
    path('routes/', views.routes, name='routes'),
    path('vehicletypes/', views.vehicle_types, name='vehicle_types'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('schedule/',views.schedule, name='schedule'),
    path('scheduledvehicles/', views.scheduled_vehicles, name='vehicle_items'),
    path('scheduledvehicles/<int:v_id>/', views.scheduled_vehicles, name='vehicle_items'),
    path('scheduledvehicles/<int:v_id>/<int:s_id>/', views.scheduled_vehicles, name='vehicle_items'),
    path('search/', views.search, name="Search"),
    path('book/', views.book, name="Booking")
    # path('book/<int:booked_id>/', views.book, name="Booking") #for future use if needed
]
