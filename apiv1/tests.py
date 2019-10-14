''' Testing module for api '''

from django.test import TestCase
from .models import Layout, Seat


class LayoutTestCase(TestCase):
    ''' Class for testing layout model '''

    def setUp(self):
        layout = Layout.objects.create(name="test_layout", seat_count=22)
        Seat.objects.create(seat_number=1, state='available', layout=layout)
        Seat.objects.create(seat_number=2, state='available', layout=layout)

    def test_layout(self):
        ''' Creates a layout and add two seats then verify if the seat count is 2 or not '''
        layout = Layout.objects.get(name="test_layout")
        for seat in layout.seat_set.all():
            print(seat)
        self.assertEqual(layout.seat_set.count(), 2)
