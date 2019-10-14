''' Utility module '''
from .models import Layout, Seat

from django.forms.models import model_to_dict as django_model_to_dict


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
        'name':layout.name,
        'data': [],
        }
    position_x = []
    position_y = []
    states = []
    for seat in seats:
        position_x.append(int(seat.row))
        position_y.append(int(seat.col))
        states.append(str(seat.state))
    for temp_x in range(max(position_x)+1):
        print(temp_x)
        response_json['data'].append([])
        for _ in range(max(position_y)+1):
            response_json['data'][temp_x].append(
                {
                    'state':"none"
                }
            )
    for n in range(len(states)):
        response_json['data'][position_x[n]][position_y[n]]['state'] = states[n]
    return response_json

def json_to_layout(data):
    ''' takes in the layout grid and creates seats with layout with it '''
    layout_name = data['name']
    layout_data = data['data']
    layout = Layout.objects.get(name=str(layout_name))
    for x in range(len(layout_data)):
        for y in range(len(layout_data[x])):
            if str(layout_data[x][y]['state']) != "none":
                temp_seat = Seat.objects.get(layout=layout, col=y, row=x)
                temp_seat.state = layout_data[x][y]['state']
                temp_seat.save()
