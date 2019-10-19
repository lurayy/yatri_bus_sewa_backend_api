''' Views module of api '''
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Layout, Route, Seat, VehicleType, Vehicle, ScheduledVehicle, Schedule, Booking
from .serializers import RouteSerializer, VehicleTypeSerializer, VehicleSerializer, ScheduledVehicleSerializer
from .utils import layout_to_json, json_to_layout, datetime_str_to_object, create_booking_instances
from .exceptions import LayoutJsonFormatException, RouteValueException, EmptyValueException
from django.db import IntegrityError


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


@require_http_methods(['GET', 'POST'])
def routes(request):
    '''
    View for handling tasks related to route model
    {
        "source":"Kathmandu",
        "destination":"Pisd"
    }
     '''
    if request.method == "POST":
        try:
            request_json = json.loads(request.body.decode('utf-8'))
            route = Route.objects.create(source=request_json['source'], destination=request_json['destination'])
            return JsonResponse({'success': 'Successfully created the route'})
        except (KeyError, json.decoder.JSONDecodeError, EmptyValueException, RouteValueException,
                IntegrityError) as exp:
            return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    response = []
    route_objects = Route.objects.all()
    for route in route_objects:
        response.append(RouteSerializer(route).data)
    return JsonResponse({'routes': response})

@require_http_methods(['GET', 'POST'])
def vehicle_types(request):
    '''
    View for handling tasks related to vehicle_type model
    Example json for post is:
    {
     "name": "TestVehicleType one",
     "layout": 1
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
     "numberPlate": "xy"
    }
    '''
    if request.method == "POST":
        try:
            request_json = json.loads(request.body.decode('utf-8'))
            vehicle_type = VehicleType.objects.get(id=request_json['vehicleType'])
            vehicle = Vehicle.objects.create(vehicle_type=vehicle_type, number_plate=request_json['numberPlate'])
            return JsonResponse({'success': 'Successfully created the vehicle'})
        except (KeyError, json.decoder.JSONDecodeError, VehicleType.DoesNotExist) as exp:
            return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    response = []
    vehicle_objects = Vehicle.objects.all()
    for vehicle in vehicle_objects:
        response.append(VehicleSerializer(vehicle).data)
    return JsonResponse({'vehicles': response})


@require_http_methods(['GET', 'POST'])
def scheduled_vehicles(request, v_id=None, s_id=None):
    '''
    View for handling tasks related to vehicle_item model
    request format:
    {
        "vehicle": 1,
        "schedule":
        [
            {
                "route":1,
                "date": "2019-11-16T08:15:00.000",
                "time": "2019-11-16T18:15:00.000",
                "nature":"Day",
            },
            {
                "route":3,
                "date": "2019-11-16T08:15:00.000",
                "time": "2019-11-16T18:15:00.000",
                "nature":"Day",
            },
            {
                "route":1,
                "date": "2019-11-16T08:15:00.000",
                "time": "2019-11-16T18:15:00.000",
                "nature":"Night",
            },
        ]
    }
    '''
    if request.method == "POST":
        try:
            request_json = json.loads(request.body.decode('utf-8'))
            scheduled_vehicle = ScheduledVehicle.objects.create(
                vehicle=Vehicle.objects.get(id=int(request_json['vehicle']))
                )
            schedule_objects = []
            for schedule_json in request_json['schedule']:
                route = Route.objects.get(id=int(schedule_json['route']))
                try:
                    schedule_objects.append(Schedule.objects.get(
                        route=route,
                        date=datetime_str_to_object(schedule_json['date']).date(),
                        time=datetime_str_to_object(schedule_json['time']).time(),
                        nature=str(schedule_json['nature'])
                    ))
                except Schedule.DoesNotExist:
                    schedule_objects.append(Schedule.objects.create(
                        route=route,
                        date=datetime_str_to_object(schedule_json['date']).date(),
                        time=datetime_str_to_object(schedule_json['time']).time(),
                        nature=str(schedule_json['nature'])
                    ))
            scheduled_vehicle.schedule.set(schedule_objects)
            scheduled_vehicle.save()
            return JsonResponse({'success': 'Successfully created the vehicle schedule'})

        except (KeyError, json.decoder.JSONDecodeError, Route.DoesNotExist, Vehicle.DoesNotExist) as exp:
            return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    response = []
    if v_id:
        try:
            s_vehicle = ScheduledVehicle.objects.get(id=int(v_id))
            response.append(ScheduledVehicleSerializer(s_vehicle).data)
            return JsonResponse({'scheduledVehicle': response[0]})
        except (KeyError, json.decoder.JSONDecodeError, ScheduledVehicle.DoesNotExist, Schedule.DoesNotExist) as exp:
            return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    scheduled_vehicle_objects = ScheduledVehicle.objects.all()
    for s_vehicle in scheduled_vehicle_objects:
        response.append(ScheduledVehicleSerializer(s_vehicle).data)
    return JsonResponse({'scheduledVehicles': response})
