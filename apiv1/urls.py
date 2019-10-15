''' Module containing the url patterns of api v1 '''

from django.urls import path
from . import views

urlpatterns = [
    path('layouts/', views.layouts, name='layouts'),
    path('routes/', views.routes, name='routes'),
    path('vehicletypes/', views.vehicle_types, name='vehicle_types'),
    path('vehicles/', views.vehicles, name='vehicles'),
]
