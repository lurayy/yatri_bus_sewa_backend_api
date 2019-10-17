''' Models module for api '''
import django
from django.db import models
from .exceptions import RouteValueException, VehicleItemException

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

    STATES = (
        ('unavailable', 'unavailable'),
        ('available', 'available'),
        ('locked', 'locked'),
        ('booked', 'booked'),
    )
    state = models.CharField(max_length=15, choices=STATES, default='available')

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
    routes = models.ManyToManyField(Route)

    def __str__(self):
        return f'Vehicle: {self.number_plate}'

    def delete(self, using=None, keep_parents=False, super_admin=None):
        if super_admin:
            super(Vehicle, self).delete()
        else:
            raise Exception('Cannot delete a read only model object')

    def save(self, *args, **kwargs):    # pylint: disable=arguments-differ
        self.number_plate = str(self.number_plate).upper()
        super(Vehicle, self).save(*args, **kwargs)


class VehicleItem(models.Model):
    ''' Store information about instance of the 'Vehicle' that is active'''
    PERIODS = (
        ('DAY', "Day"),
        ('NIGHT', "Night")
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    departure_point = models.CharField(max_length=255)
    departure_period = models.CharField(max_length=6, choices=PERIODS, default='DAY')
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):    # pylint: disable=arguments-differ
        if not str(self.departure_point).strip():
            raise VehicleItemException('Departure Point Cannot be empty.')
        self.departure_point = str(self.departure_point).lower().title()
        if not self.pk:
            super(VehicleItem, self).save(*args, **kwargs)
            seats = self.vehicle.vehicle_type.layout.seat_set.all()
            for seat in seats:
                SeatItem.objects.create(vehicle_item=self, label=seat.label, state=seat.state)
        else:
            super(VehicleItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'VehicleItem: {self.vehicle}, {self.departure_date}'


class Booking(models.Model):
    ''' Stores booking details'''
    booked_by = models.CharField(max_length=255)            # will be a linked to user profile in future
    booked_for = models.CharField(max_length=255)
    total_amount_paid = models.PositiveIntegerField()
    is_paid = models.BooleanField()                         # will be a selection after we decide what to implement
    payment_method = models.CharField(max_length=255)
    date = models.DateTimeField(default=django.utils.timezone.now)
    # for ease of info extraction i.e bus number
    vehicle_item = models.ForeignKey(VehicleItem, on_delete=models.SET_NULL, null=True)


class SeatItem(models.Model):
    ''' Seat  Instance linked to the active vehicle instance and layout instance '''
    vehicle_item = models.ForeignKey(VehicleItem, on_delete=models.CASCADE, related_name='seat_items')
    label = models.CharField(max_length=5, null=True)
    STATES = (
        ('unavailable', 'unavailable'),
        ('available', 'available'),
        ('locked', 'locked'),
        ('booked', 'booked'),
    )
    state = models.CharField(max_length=15, choices=STATES, default='available')
    booking_details = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return f'SeatItem: {self.vehicle_item}, {self.label}'
