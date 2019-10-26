''' Utility module '''
from django.forms.models import model_to_dict as django_model_to_dict
import dateutil.parser
# import dateutil.parser
from .models import Layout, Seat, Booking
from .exceptions import LayoutJsonFormatException


def model_to_dict(class_name):
    ''' Returns the dictionary of dialog objects '''
    objects = class_name.objects.all()
    object_list = []
    for obj in objects:
        object_list.append(django_model_to_dict(obj))
    return object_list


def layout_to_json(layout):
    ''' Takes in layout objects and gives all the data related to layout and it's seats'''
    seats = Seat.objects.filter(layout=layout)
    response_json = {
        'id': layout.id,
        'name': layout.name,
        'data': [],
    }
    if seats.count() == 0:
        return response_json
    position_x = []
    position_y = []
    labels = []
    for seat in seats:
        position_x.append(int(seat.row))
        position_y.append(int(seat.col))
        labels.append(str(seat.label))
    for temp_x in range(max(position_x)+1):
        response_json['data'].append([])
        for _ in range(max(position_y)+1):
            response_json['data'][temp_x].append(
                {
                    'is_active': False,
                    'label': "none"
                }
            )
    for index, label in enumerate(labels):
        response_json['data'][position_x[index]][position_y[index]]['label'] = label
        response_json['data'][position_x[index]][position_y[index]]['is_active'] = True
    return response_json


def json_to_layout(data):
    ''' takes in the layout grid and creates seats with layout with it '''
    layout_name = data['name']
    layout_data = data['data']
    if layout_name == "":
        raise LayoutJsonFormatException("Layout name is needed to create a layout")
    layout = Layout.objects.create(name=str(layout_name))
    for x_index, row in enumerate(layout_data):
        for y_index, cell in enumerate(row):
            if cell['is_active']:
                temp_seat = Seat(layout=layout, col=y_index, row=x_index)
                temp_seat.label = cell['label']
                temp_seat.save()
    return layout

def datetime_str_to_object(date_str):
    ''' Parses datetime string to datetime object '''
    return dateutil.parser.parse(date_str)

def create_booking_instances(scheduled_vehicle):
    ''' Function to initilze all the booking (seats) for the schedule vehicles'''
    layout = scheduled_vehicle.vehicle.vehicle_type.layout
    seats = Seat.objects.filter(layout=layout)
    for seat in seats:
        Booking.objects.create(seat=seat, trip=scheduled_vehicle)


def get_seat_booking(trip, schedule):
    ''' Takes in layout objects and gives all the data related to layout and it's seats'''
    seats = Seat.objects.filter(layout=trip.vehicle.vehicle_type.layout)
    response_json = []
    if seats.count() == 0:
        return response_json
    position_x = []
    position_y = []
    states = []
    for seat in seats:
        position_x.append(int(seat.row))
        position_y.append(int(seat.col))
        try:
            state = Booking.objects.get(seat=seat, trip=trip, schedule=schedule).state
        except Booking.DoesNotExist:
            state = 'available'
        states.append(str(state))
    for temp_x in range(max(position_x)+1):
        response_json.append([])
        for _ in range(max(position_y)+1):
            response_json[temp_x].append(
                {
                    'state': "none"
                }
            )
    for index, state in enumerate(states):
        response_json[position_x[index]][position_y[index]]['state'] = state
    return response_json
