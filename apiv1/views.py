''' Views module of api '''
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Layout, Route, VehicleType, Vehicle
from .serializers import RouteSerializer, VehicleTypeSerializer, VehicleSerializer
from .utils import layout_to_json, json_to_layout


@require_http_methods(['GET', 'POST'])
def layouts(request):
    ''' View for handling tasks related to layout model '''
    if request.method == "POST":
        try:
            request_json = json.loads(request.body.decode('utf-8'))
            json_to_layout(request_json)
            return JsonResponse({'success': 'Successfully created the layout'})
        except (KeyError, json.decoder.JSONDecodeError, Exception) as exp:
            return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    response = []
    layout_objects = Layout.objects.all()
    for layout in layout_objects:
        response.append(layout_to_json(layout))
    return JsonResponse({'layouts': response})


@require_http_methods(['GET'])
def routes(request):
    ''' View for handling tasks related to route model '''
    response = []
    route_objects = Route.objects.all()
    for route in route_objects:
        response.append(RouteSerializer(route))
    return JsonResponse({'routes': response})


@require_http_methods(['GET', 'POST'])
def vehicle_types(request):
    '''
    View for handling tasks related to vehicle_type model
    Example json for post is:
    {
     "name": name,
     "layout": 1,
    }
    '''
    if request.method == "POST":
        try:
            request_json = json.loads(request.body.decode('utf-8'))
            layout = Layout.objects.get(id=request_json['layout'])
            VehicleType.objects.create(name=request_json['name'], layout=layout)
            return JsonResponse({'success': 'Successfully created the vehicle type'})
        except (KeyError, json.decoder.JSONDecodeError, Layout.DoesNotExist) as exp:
            return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    response = []
    vehicle_type_objects = VehicleType.objects.all()
    for vehicle_type in vehicle_type_objects:
        response.append(VehicleTypeSerializer(vehicle_type).data)
    return JsonResponse({'vehicleTypes': response})


@require_http_methods(['GET', 'POST'])
def vehicles(request):
    '''
    View for handling tasks related to vehicle model
    Example json for post is:
    {
     "vehicleType": 1,
     "numberPlate": "xy",
     "routes":[
         {
             "source":"Pokahra",
             "destination":"Kathmand"
         },
         {
             "source":"Pokahra",
             "destination":"Kathmandu"
         },
         {
             "source":"Nepal",
             "destination":"India"
         }
     ]
    }
    '''
    if request.method == "POST":
        try:
            request_json = json.loads(request.body.decode('utf-8'))
            vehicle_type = VehicleType.objects.get(id=request_json['vehicleType'])
            vehicle = Vehicle.objects.create(vehicle_type=vehicle_type, number_plate=request_json['numberPlate'])
            routes_objects = []
            for temp_routes in request_json['routes']:
                try:
                    temp_route_object = Route.objects.get(
                        source=str(temp_routes['source']).lower().title(),
                        destination=str(temp_routes['destination']).lower().title())
                except Route.DoesNotExist:
                    temp_route_object = Route.objects.create(
                        source=str(temp_routes['source']),
                        destination=str(temp_routes['destination']))
                routes_objects.append(temp_route_object)
            vehicle.routes.set(routes_objects)
            return JsonResponse({'success': 'Successfully created the vehicle'})
        except (KeyError, json.decoder.JSONDecodeError, VehicleType.DoesNotExist) as exp:
            return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})

    response = []
    vehicle_objects = Vehicle.objects.all()
    for vehicle in vehicle_objects:
        response.append(VehicleSerializer(vehicle).data)
    return JsonResponse({'vehicles': response})
