''' Models module for api '''
import django
from django.db import models
from .exceptions import RouteValueException, EmptyValueException

class Layout(models.Model):
    ''' Information about Seat layout '''
    REQUIRED_FIELDS = ('name',)

    name = models.CharField(max_length=255)

    def __str__(self):
        return f'Layout: {self.name}, {self.seat_set.count()} seats'

    def delete(self, using=None, keep_parents=False):
        raise Exception('Cannot delete a read only model object')

    def save(self, *args, **kwargs):    # pylint: disable=arguments-differ
        if self.name == "":
            raise Exception('Cannot save layout with no name')
        self.name = str(self.name).lower().title()
        super(Layout, self).save(*args, **kwargs)


class Seat(models.Model):
    '''Seat related with layout'''
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE)
    label = models.CharField(max_length=5, default=None, blank=True, null=True)
    col = models.PositiveIntegerField()
    row = models.PositiveIntegerField()

    def __str__(self):
        return f'Seat: {self.layout.name}, {self.label}'

    def delete(self, using=None, keep_parents=False):
        raise Exception('Cannot delete a read only model object')


class VehicleType(models.Model):
    ''' For Storing data about the vehicle type.'''
    name = models.CharField(max_length=255)
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        raise Exception('Cannot delete a read only model object')

    def save(self, *args, **kwargs):    # pylint: disable=arguments-differ
        self.name = str(self.name).lower().title()
        super(VehicleType, self).save(*args, **kwargs)


class Route(models.Model):
    ''' Basic information about the route that the vehicle will take.'''
    REQUIRED_FIELDS = ('source', 'destination',)
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)

    def delete(self, using=None, keep_parents=False):
        raise Exception('Cannot delete a read only model object')

    class Meta:
        unique_together = ['source', 'destination']

    def save(self, *args, **kwargs):    # pylint: disable=arguments-differ
        if not str(self.source).strip() or not str(self.destination).strip():
            raise RouteValueException('Neither Route source nor Route destination can be empty.')
        if str(self.source).lower().strip() == str(self.destination).lower().strip():
            raise RouteValueException('Souce and Destination of Route cannot be same.')
        self.source = str(self.source).lower().title()
        self.destination = str(self.destination).lower().title()
        super(Route, self).save(*args, **kwargs)

    def __str__(self):
        return self.source + " : " + self.destination

class Vehicle(models.Model):
    ''' Stores information about a particular vehicle'''
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE,)
    number_plate = models.CharField(max_length=255)

    def __str__(self):
        return f'Vehicle: {self.number_plate}'

    def delete(self, using=None, keep_parents=False, super_admin=None): # pylint: disable=arguments-differ
        if super_admin:
            super(Vehicle, self).delete()
        else:
            raise Exception('Cannot delete a read only model object')

    def save(self, *args, **kwargs):    # pylint: disable=arguments-differ
        self.number_plate = str(self.number_plate).upper()
        super(Vehicle, self).save(*args, **kwargs)


class ActiveDateTime(models.Model):
    ''' Model to store date time '''
    date = models.DateField()
    time = models.TimeField()
    PERIODS = (
        ('DAY', "Day"),
        ('NIGHT', "Night")
    )
    period = models.CharField(max_length=6, choices=PERIODS, default='DAY')

class PickUpPoint(models.Model):
    ''' Model to store pickup point info '''
    name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):    # pylint: disable=arguments-differ
        if not str(self.name).strip():
            raise EmptyValueException('Departure Point Cannot be empty.')
        self.name = str(self.name).lower().title()


class ScheduledVehicle(models.Model):
    ''' Store information about instance of the 'Vehicle' that is active'''
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True)
    active_stages = models.ManyToManyField(ActiveDateTime)
    pick_up_points = models.ManyToManyField(PickUpPoint)

    def __str__(self):
        return f'VehicleItem: {self.vehicle}'


class Booking(models.Model):
    ''' Stores booking details'''
    trip = models.ForeignKey(ScheduledVehicle, on_delete=models.SET_NULL, null=True)
    booked_by = models.CharField(max_length=255)            # will be a linked to user profile in future
    passenger_name = models.CharField(max_length=255)
    passenger_phone = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    is_paid = models.BooleanField()                         # will be a selection after we decide what to implement
    payment_method = models.CharField(max_length=255)
    date = models.DateTimeField(default=django.utils.timezone.now)
    STATES = (
        ('unavailable', 'unavailable'),
        ('available', 'available'),
        ('locked', 'locked'),
        ('booked', 'booked'),
    )
    state = models.CharField(max_length=15, choices=STATES, default='available')
    