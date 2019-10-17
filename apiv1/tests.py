''' Testing module for api '''
import json
from datetime import date, time

from django.test import TestCase, Client, RequestFactory

from .models import Layout, Route, Seat, Vehicle, VehicleItem, VehicleType
from .utils import layout_to_json, json_to_layout

from .views import vehicle_items


LAYOUT_DATA = {
    'id': 1,
    'name': 'Super Deluxe Layout',
    'data': [
        [{'state': 'available', 'label':'A'}],
        [{'state': 'available', 'label':'B'}]]
}

VEHICLE_ITEM_DATA = {
        "vehicle": 1,
        "departureTime": "2019-11-16T18:15:00.000",
        "departurePoint": "somePlace",
        "vehicleItems": [
            {
                "departureDate": "2019-11-16T08:15:00.000",
                "route":1,
                "departurePeriod":"Day"
            },
            {
                "departureDate": "2019-11-17T18:15:00.000",
                "route":2,
                "departurePeriod":"Night"
            },
            {
                "departureDate": "2019-11-19T08:15:00.000",
                "route":1,
                "departurePeriod":"Day"
            }
        ]
    }

class LayoutTestCase(TestCase):
    ''' Class for testing layout model '''

    def setUp(self):
        layout = Layout.objects.create(name='Super Deluxe Layout')
        Seat.objects.create(col=0, row=0, state='available', label='A', layout=layout)
        Seat.objects.create(col=0, row=1, state='available', label='B', layout=layout)

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
        Seat.objects.create(col=0, row=1, label='A', state='available', layout=layout)
        Seat.objects.create(col=0, row=0, label='B',state='available', layout=layout)
        vehicle_type = VehicleType.objects.create(name='Super Deluxe', layout=layout)
        route = Route.objects.create(source='Pokhara', destination='Kathmandu')
        vehicle = Vehicle.objects.create(vehicle_type=vehicle_type, number_plate='GA15')
        vehicle.routes.add(route)
        vehicle.save()
        self.vehicle_item = VehicleItem.objects.create(
            vehicle=vehicle,
            departure_date=date(2019, 10, 14), departure_time=time(12, 23, 12), departure_point='Bhairab tole',
            departure_period="Day", route=route)

    def test_layout(self):
        ''' Creates a vehicle item object and verifies by priting the seat items '''
        self.assertEqual(self.vehicle_item.vehicle.vehicle_type.layout.name, 'Super Deluxe Layout')

class RequestTestCase(TestCase):
    ''' Testcase class for functions on views '''
    def setUp(self):
        self.client = Client()
        layout = Layout.objects.create(name='Super Deluxe Layout')
        Seat.objects.create(col=0, row=1, label='A', state='available', layout=layout)
        Seat.objects.create(col=0, row=0, label='B', state='available', layout=layout)
        vehicle_type = VehicleType.objects.create(name='Super Deluxe', layout=layout)
        route1 = Route.objects.create(source='Pokhara', destination='Kathmandu')
        route2 = Route.objects.create(source='Kathmandu', destination='Pokhara')
        vehicle = Vehicle.objects.create(vehicle_type=vehicle_type, number_plate='GA15')
        vehicle.routes.add(route1)
        vehicle.routes.add(route2)
        vehicle.save()

    def test_vehicle_items_post(self):
        ''' Tests vehicle_items post function '''
        body = json.dumps(VEHICLE_ITEM_DATA)
        response = self.client.post('/api/v1/vehicleitems/', body, content_type='application/json')
        self.assertEqual(response.json(), {'success': 'Successfully created the vehicleItem.'})
