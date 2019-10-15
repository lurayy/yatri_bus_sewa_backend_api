''' Testing module for api '''
import json
from datetime import date, time

from django.test import TestCase, Client

from .models import Layout, Route, Seat, Vehicle, VehicleItem, VehicleType
from .utils import layout_to_json, json_to_layout

LAYOUT_DATA = {
    'name': 'Super Deluxe Layout',
    'data': [
        [{'state': 'available'}],
        [{'state': 'available'}]]
}


class LayoutTestCase(TestCase):
    ''' Class for testing layout model '''

    def setUp(self):
        layout = Layout.objects.create(name='Super Deluxe Layout')
        Seat.objects.create(col=0, row=0, state='available', layout=layout)
        Seat.objects.create(col=0, row=1, state='available', layout=layout)

    def test_layout(self):
        ''' Creates a layout and add two seats then verify if the seat count is 2 or not '''
        layout = Layout.objects.get(name='Super Deluxe Layout')
        self.assertEqual(layout.seat_set.count(), 2)

    def test_layout_to_json(self):
        ''' Tests layout to json function '''
        layout = Layout.objects.get(name='Super Deluxe Layout')
        self.assertEqual(layout_to_json(layout), LAYOUT_DATA)

    def test_json_to_layout(self):
        ''' Tests layout to json function '''
        layout = json_to_layout(LAYOUT_DATA)
        self.assertEqual(layout.name, 'Super Deluxe Layout')
        self.assertEqual(layout.seat_set.count(), 2)
        self.assertEqual(layout.seat_set.all()[0].col, 0)
        self.assertEqual(layout.seat_set.all()[0].row, 0)
        self.assertEqual(layout.seat_set.all()[1].col, 0)
        self.assertEqual(layout.seat_set.all()[1].row, 1)

    def test_get_layouts_view(self):
        ''' Tests get layouts view '''
        client = Client()
        response = client.get('/api/v1/layouts/')
        self.assertEqual(response.json(), {'layouts': [LAYOUT_DATA]})


class VehicleItemTestCase(TestCase):
    ''' Class for testing vehicle item model '''

    def setUp(self):
        layout = Layout.objects.create(name='Super Deluxe Layout')
        Seat.objects.create(col=0, row=1, state='available', layout=layout)
        Seat.objects.create(col=0, row=0, state='available', layout=layout)
        vehicle_type = VehicleType.objects.create(name='Super Deluxe', layout=layout)
        route = Route.objects.create(source='Pokhara', destination='Kathmandu')
        vehicle = Vehicle.objects.create(vehicle_type=vehicle_type, number_plate='GA15')
        vehicle.routes.add(route)
        vehicle.save()
        self.vehicle_item = VehicleItem.objects.create(
            vehicle=vehicle,
            departure_date=date(2019, 10, 14), departure_time=time(12, 23, 12), departure_point='Bhairab tole')

    def test_layout(self):
        ''' Creates a vehicle item object and verifies by priting the seat items '''
        self.assertEqual(self.vehicle_item.vehicle.vehicle_type.layout.name, 'Super Deluxe Layout')
