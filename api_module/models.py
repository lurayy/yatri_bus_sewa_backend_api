from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
import django
import json 


class Layout(models.Model):
    ''' Information about Seat layout '''
    name = models.CharField(max_length=255)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    grid = models.TextField()

    def __str__(self):
        return str(self.name)

class VehicleType(models.Model):
    ''' For Storing data about the vehicle type.'''
    name = models.CharField(max_length = 255)
    seat_count = models.PositiveIntegerField()
    layout = models.ForeignKey(Layout, on_delete = models.SET_NULL, null = True)

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
    vehicle_type = models.ForeignKey(VehicleType, on_delete = models.SET_NULL, null = True)
    number_plate = models.CharField(max_length=255)


class ActiveVehicle(models.Model):
    ''' Store information about instance of the 'Vehicle' that is active'''
    vehicle = models.ForeignKey(Vehicle, on_delete = models.SET_NULL, null = True)
    route = models.ForeignKey(Route, on_delete = models.SET_NULL, null = True)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    departure_point = models.CharField(max_length=255)
    # driver = link driver profile here

    def save(self, *args, **kwargs):
        if not self.pk:
            print("Creating new active vehicle")
            super(ActiveVehicle, self).save(*args, **kwargs)
            layout = json.loads(self.vehicle.vehicle_type.layout.grid)
            for x in range (len(layout)):
                for y in range (len(layout[x])):
                    if str(layout[x][y]['state']) == "available":
                        s = Seat(vehicle = self, seat_number = str(x)+","+str(y))
                        s.save()
        else:
            super(ActiveVehicle, self).save(*args, **kwargs)



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
    seat_number = models.CharField(max_length=5)
    STATES = (
        ('unavailable', 'unavailable'),
        ('available', 'available'),
        ('locked', 'locked'),
        ('booked', 'booked'),
    )
    state = models.CharField(max_length=15, choices= STATES, default='available')
    booking_details = models.ForeignKey(Booking, on_delete = models.SET_NULL, null = True, default = None)
