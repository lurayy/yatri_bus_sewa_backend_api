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

# data = {
#   "name": "hello world",
#   "data": [
#     [
#       {
#         "state": "available"
#       },
#       {
#         "state": "available"
#       }
#     ],
#     [
#       {
#         "state": "available"
#       },
#       {
#         "state": "none"
#       }
#     ]
#   ]
# }

# def layout_to_json(layout):
#     seats = Seat.objects.filter(layout = layout)
#     response_json = {
#         'name': layout.name,
#         'data':[
#             [

#             ]
#         ]
#     }
#     for seat in seats:
        


# def json_to_layout(data):
#     pass