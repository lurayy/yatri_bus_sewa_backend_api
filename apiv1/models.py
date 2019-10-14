from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
import django
import json 


class Layout(models.Model):
    ''' Information about Seat layout '''
    name = models.CharField(max_length=255)
    seat_count = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name + " : "+str(self.seat_count)

class LayoutItem(models.Model):
    ''' Safe version of layout model that is used for linking to the bus item'''
    name = models.CharField(max_length=255)

    def __str__(self):
        return  str(self.name)
    

class Seat(models.Model):
    '''Seat related with layout'''
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    STATES = (
        ('unavailable', 'unavailable'),
        ('available', 'available'),
        ('locked', 'locked'),
        ('booked', 'booked'),
    )
    state = models.CharField(max_length=15, choices= STATES, default='available')
    
    def __str__(self):
        return self.layout.name + ": " + self.seat_number



class VehicleType(models.Model):
    ''' For Storing data about the vehicle type.'''
    name = models.CharField(max_length = 255)
    layout = models.ForeignKey(Layout, on_delete = models.SET_NULL, null = True)

class Route(models.Model):
    ''' Basic information about the route that the vehicle will take.'''
    origin = models.CharField(max_length = 255)
    destination = models.CharField(max_length = 255)
    
    def delete(self, *args, **kwargs):
        raise Exception("Cannot Delete Read Only Models.")

class Vehicle(models.Model):
    ''' Stores information about a particular vehicle'''
    vehicle_type = models.ForeignKey(VehicleType, on_delete = models.SET_NULL, null = True)
    number_plate = models.CharField(max_length=255)

    def __str__(self):
        return self.number_plate


class VehicleItem(models.Model):
    ''' Store information about instance of the 'Vehicle' that is active'''
    vechicle = models.ForeignKey(Vehicle, on_delete = models.SET_NULL, null = True)

    route = models.ForeignKey(Route, on_delete = models.SET_NULL, null = True)
    # duplicate data for integrity
    layout_item = models.ForeignKey(LayoutItem, on_delete= models.SET_DEFAULT, blank=True, null=True, default = None)

    departure_date = models.DateField()
    departure_time = models.TimeField()
    departure_point = models.CharField(max_length=255)
    # driver = link driver profile here

    def save(self, *args, **kwargs):
        if not self.pk:
            print("Creating new active vehicle")
            super(VehicleItem, self).save(*args, **kwargs)

            # Creating LayoutItem and linking it with VehicleItem
            read_only_layout = self.vechicle.vehicle_type.layout
            layout = LayoutItem(name = read_only_layout.name)
            layout.save()
            self.layout_item = layout
            self.save()

            # Creating Seats Using the given layout
            seats = Seat.objects.filter(layout = read_only_layout)
            for seat in seats:
                seat_item = SeatItem.objects.create(layout_item = self.layout_item, vehicle_item= self, seat_number = seat.seat_number, state = seat.state)
                seat_item.save()

        else:
            super(VehicleItem, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.vechicle) + " " + str(self.departure_date) 

class Booking(models.Model):
    ''' Stores booking details'''
    booked_by = models.CharField(max_length= 255)                                          # will be a linked to user profile in future
    booked_for = models.CharField(max_length=255)
    total_amount_paid = models.PositiveIntegerField()
    is_paid = models.BooleanField()
    payment_method = models.CharField(max_length= 255)                                     # will be a selection after we decide what to implement
    date = models.DateTimeField(default = django.utils.timezone.now)
    vehicle_item = models.ForeignKey(VehicleItem, on_delete = models.SET_NULL, null = True)   # for ease of info extraction i.e bus number


class SeatItem(models.Model):
    ''' Seat  Instance linked to the active vehicle instance and layout instance '''
    layout_item = models.ForeignKey(LayoutItem, on_delete = models.CASCADE)
    vehicle_item = models.ForeignKey(VehicleItem, on_delete = models.CASCADE)
    seat_number = models.CharField(max_length=5)
    STATES = (
        ('unavailable', 'unavailable'),
        ('available', 'available'),
        ('locked', 'locked'),
        ('booked', 'booked'),
    )
    state = models.CharField(max_length=15, choices= STATES, default='available')
    booking_details = models.ForeignKey(Booking, on_delete = models.SET_NULL, null = True, default = None)

    def __str__(self):
        return str(self.vehicle_item) + ": " + self.seat_number
