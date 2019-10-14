''' Testing module for api '''
from datetime import date, time

from django.test import TestCase

from .models import Layout, Route, Seat, Vehicle, VehicleItem, VehicleType


class LayoutTestCase(TestCase):
    ''' Class for testing layout model '''

    def setUp(self):
        layout = Layout.objects.create(name='Super Deluxe Layout')
        Seat.objects.create(col=0, row=0, state='available', layout=layout)
        Seat.objects.create(col=0, row=1, state='available', layout=layout)

    def test_layout(self):
        ''' Creates a layout and add two seats then verify if the seat count is 2 or not '''
        layout = Layout.objects.get(name='Super Deluxe Layout')
        for seat in layout.seat_set.all():
            print(seat)
        self.assertEqual(layout.seat_set.count(), 2)


class VehicleItemTestCase(TestCase):
    ''' Class for testing vehicle item model '''

    def setUp(self):
        layout = Layout.objects.create(name='Super Deluxe Layout')
        Seat.objects.create(col=0, row=1, state='available', layout=layout)
        Seat.objects.create(col=0, row=0, state='available', layout=layout)
        vehicle_type = VehicleType.objects.create(name='Super Deluxe', layout=layout)
        route = Route.objects.create(source='Pokhara', destination='Kathmandu')
        vehicle = Vehicle.objects.create(vehicle_type=vehicle_type, number_plate='GA15')
        self.vehicle_item = VehicleItem.objects.create(
            vehicle=vehicle, route=route,
            departure_date=date(2019, 10, 14), departure_time=time(12, 23, 12), departure_point='Bhairab tole')

    def test_layout(self):
        ''' Creates a vehicle item object and verifies by priting the seat items '''
        print(self.vehicle_item)
        for seat_item in self.vehicle_item.seat_item_set.all():
            print(seat_item)
        self.assertEqual(self.vehicle_item.vehicle.vehicle_type.layout.name, 'Super Deluxe Layout')
