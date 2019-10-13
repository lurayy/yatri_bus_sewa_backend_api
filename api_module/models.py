from django.db import models
from django.contrib.auth.models import AbstractUser
import django

class VehicleType(models.Model):
    ''' For Storing data about the vehicle type.'''
    name = models.CharField(max_length = 255)
    seat_count = models.PositiveIntegerField()
    seat_x = models.PositiveIntegerField()
    seat_y = models.PositiveIntegerField()


class Route(models.Model):
    ''' Basic information about the route that the vehicle will take.'''
    origin = models.CharField(max_length = 255)
    destination = models.CharField(max_length = 255)
    # For future use 
    # pickup_points = ArrayField(
    #     ArrayField(
    #         models.CharField(max_length= 255, blank= True),
    #         size = 12,
    #     ),
    #     ArrayField(
    #         models.DateTimeField(),
    #         size = 12,
    #     ),
    #     default = None
    # )
    # droping_points = ArrayField(
    #     ArrayField(
    #         models.CharField(max_length= 255, blank= True),
    #         size = 12,
    #     ),
    #     ArrayField(
    #         models.DateTimeField(),
    #         size = 12,
    #     ),
    #     default = None
    # )


class Vehicle(models.Model):
    ''' Stores information about a particular vehicle'''
    bus_type = models.ForeignKey(VehicleType, on_delete = models.SET_NULL, null = True)
    number_plate = models.CharField(max_length=255)


class ActiveVehicle(models.Model):
    ''' Store information about instance of the 'Vehicle' that is active'''
    vehicle = models.ForeignKey(Vehicle, on_delete = models.SET_NULL, null = True)
    route = models.ForeignKey(Route, on_delete = models.SET_NULL, null = True)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    departure_point = models.CharField(max_length=255)
    # driver = link driver profile here


class Booking(models.Model):
    ''' Stores booking details'''
    booked_by = models.CharField(max_length= 255)                                          # will be a linked to user profile in future
    booked_for = models.CharField(max_length=255)
    total_amount_paid = models.PositiveIntegerField()
    is_paid = models.BooleanField()
    payment_method = models.CharField(max_length= 255)                                     # will be a selection after we decide what to implement
    date = models.DateTimeField(default = django.utils.timezone.now)
    vehicle = models.ForeignKey(ActiveVehicle, on_delete = models.SET_NULL, null = True)   # for ease of info extraction i.e bus number


class Seat(models.Model):
    ''' Seat linked to the active vehicle instance and is created dynamically using information for VehicleType'''
    vehicle = models.ForeignKey(ActiveVehicle, on_delete = models.CASCADE)
    number = models.CharField(max_length=5)
    is_active = models.BooleanField(default = True)
    booking_details = models.ForeignKey(Booking, on_delete = models.SET_NULL, null = True, default = None)
