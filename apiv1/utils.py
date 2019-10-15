''' Utility module '''
from django.forms.models import model_to_dict as django_model_to_dict

from .models import Layout, Seat


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
    states = []
    for seat in seats:
        position_x.append(int(seat.row))
        position_y.append(int(seat.col))
        states.append(str(seat.state))
    for temp_x in range(max(position_x)+1):
        response_json['data'].append([])
        for _ in range(max(position_y)+1):
            response_json['data'][temp_x].append(
                {
                    'state': "none"
                }
            )
    for index, state in enumerate(states):
        response_json['data'][position_x[index]][position_y[index]]['state'] = state
    return response_json


def json_to_layout(data):
    ''' takes in the layout grid and creates seats with layout with it '''
    layout_name = data['name']
    layout_data = data['data']
    layout = Layout.objects.create(name=str(layout_name))
    for x_index, row in enumerate(layout_data):
        for y_index, cell in enumerate(row):
            if str(cell['state']) != "none":
                temp_seat = Seat(layout=layout, col=y_index, row=x_index)
                temp_seat.state = cell['state']
                temp_seat.save()
    return layout
