''' Views module of api '''
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Layout, Route, VehicleType, Vehicle, ScheduledVehicle, Route
from .serializers import RouteSerializer, VehicleTypeSerializer, VehicleSerializer
from .utils import layout_to_json, json_to_layout, datetime_str_to_object
from .exceptions import LayoutJsonFormatException, RouteValueException, EmptyValueException


@require_http_methods(['GET', 'POST'])
def layouts(request):
    ''' View for handling tasks related to layout model
    
    {
        "name": "Test Layout two",
        "data": [
          [
            { "is_active": true, "label": "a" },
            { "is_active": true, "label": "b" },
            { "is_active": true, "label": "c" },
            { "is_active": true, "label": "d" },
            { "is_active": true, "label": "e" },
            { "is_active": true, "label": "f" }
          ],
          [
            { "is_active": true, "label": "g" },
            { "is_active": false, "label": "h" },
            { "is_active": false, "label": "i" },
            { "is_active": false, "label": "j" },
            { "is_active": false, "label": "k" },
            { "is_active": false, "label": "l" }
          ],
          [
            { "is_active": true, "label": "m" },
            { "is_active": true, "label": "n" },
            { "is_active": true, "label": "o" },
            { "is_active": true, "label": "p" },
            { "is_active": true, "label": "q" },
            { "is_active": true, "label": "r" }
          ]
        ]
      }
    '''
    if request.method == "POST":
        try:
            request_json = json.loads(request.body.decode('utf-8'))
            json_to_layout(request_json)
            return JsonResponse({'success': 'Successfully created the layout'})
        except (KeyError, json.decoder.JSONDecodeError, LayoutJsonFormatException) as exp:
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
    # if request.method == "POST":
    #     try:
    #         request_json = json.loads(request.body.decode('utf-8'))
    #         layout = Layout.objects.get(id=request_json['layout'])
    #         VehicleType.objects.create(name=request_json['name'], layout=layout)
    #         return JsonResponse({'success': 'Successfully created the vehicle type'})
    #     except (KeyError, json.decoder.JSONDecodeError, Layout.DoesNotExist) as exp:
    #         return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    # response = []
    # vehicle_type_objects = VehicleType.objects.all()
    # for vehicle_type in vehicle_type_objects:
    #     response.append(VehicleTypeSerializer(vehicle_type).data)
    # return JsonResponse({'vehicleTypes': response})
    pass

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
    # if request.method == "POST":
    #     try:
    #         request_json = json.loads(request.body.decode('utf-8'))
    #         vehicle_type = VehicleType.objects.get(id=request_json['vehicleType'])
    #         vehicle = Vehicle.objects.create(vehicle_type=vehicle_type, number_plate=request_json['numberPlate'])
    #         routes_objects = []
    #         for temp_routes in request_json['routes']:
    #             try:
    #                 temp_route_object = Route.objects.get(
    #                     source=str(temp_routes['source']).lower().title(),
    #                     destination=str(temp_routes['destination']).lower().title())
    #             except Route.DoesNotExist:
    #                 try:
    #                     temp_route_object = Route.objects.create(
    #                         source=str(temp_routes['source']),
    #                         destination=str(temp_routes['destination']))
    #                 except RouteValueException as exp:
    #                     vehicle.delete(super_admin=True)
    #                     return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    #             routes_objects.append(temp_route_object)
    #         vehicle.routes.set(routes_objects)
    #         return JsonResponse({'success': 'Successfully created the vehicle'})
    #     except (KeyError, json.decoder.JSONDecodeError, VehicleType.DoesNotExist) as exp:
    #         return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    pass
    # response = []
    # vehicle_objects = Vehicle.objects.all()
    # for vehicle in vehicle_objects:
    #     response.append(VehicleSerializer(vehicle).data)
    # return JsonResponse({'vehicles': response})


@require_http_methods(['GET', 'POST'])
def vehicle_items(request, v_id=None):
    '''
    View for handling tasks related to vehicle_item model
    request format:
    {
        "vehicle": 1,
        "departureTime": "2019-11-16T18:15:00.000",
        "departurePoint": "somePlace",
        "vehicleItems": [
            {
            "departureDate": "2019-11-16T08:15:00.000",
            "route":1,
            "departurePeriod":"Day",
            },{
            "departureDate": "2019-11-17T18:15:00.000",
            "route":2,
            "departurePeriod":"Night",
            },{
            "departureDate": "2019-11-19T08:15:00.000",
            "route":1,
            "departurePeriod":"Day",
            }
        ]
    }
    '''
    # if request.method == "POST":
    #     request_json = json.loads(request.body.decode('utf-8'))
    #     try:
    #         vehicle = Vehicle.objects.get(id=int(request_json['vehicle']))
    #         departure_time = datetime_str_to_object(request_json['departureTime']).time()
    #         for item_data in request_json['vehicleItems']:
    #             VehicleItem.objects.create(vehicle=vehicle,
    #                                        departure_date=datetime_str_to_object(item_data['departureDate']).date(),
    #                                        departure_time=departure_time,
    #                                        departure_point=str(request_json['departurePoint']),
    #                                        departure_period=str(item_data['departurePeriod']),
    #                                        route=Route.objects.get(id=int(item_data['route']))
    #                                        )
    #         return JsonResponse({'success': 'Successfully created the vehicleItem.'})
    #     except(KeyError, json.decoder.JSONDecodeError, Vehicle.DoesNotExist, EmptyValueException,
    #            Route.DoesNotExist) as exp:
    #         return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})

    # response = []
    # try:
    #     vehicle_item = VehicleItem.objects.get(id=v_id)
    #     response.append(VehicleItemSerializer(vehicle_item).data)
    #     return JsonResponse({'vehicleItems': response})
    # except VehicleItem.DoesNotExist:
    #     return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    pass