''' Views module of api '''
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Layout, Route, Seat, VehicleType, Vehicle, ScheduledVehicle, Schedule, Booking
from .serializers import RouteSerializer, VehicleTypeSerializer, VehicleSerializer, ScheduledVehicleSerializer, ScheduleSerializer
from .utils import layout_to_json, json_to_layout, datetime_str_to_object, create_booking_instances, get_seat_booking
from .exceptions import LayoutJsonFormatException, RouteValueException, EmptyValueException
from django.db import IntegrityError
from users.models import CustomUserBase

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

def schedule(request):
    response = []
    for schedule_object in Schedule.objects.all():
        response.append(ScheduleSerializer(schedule_object).data)
    return JsonResponse({'schedule':response})

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
            response = {'scheduledVehicle':'', 'booked_seats':''}
            scheduled_vehicle_object = ScheduledVehicle.objects.get(id=v_id)
            response['scheduledVehicle'] = (ScheduledVehicleSerializer(scheduled_vehicle_object).data)
            if s_id:
                schedule_object = Schedule.objects.get(id=s_id)
                booked_seats = get_seat_booking(scheduled_vehicle_object, schedule_object)
                response['scheduledVehicle']['schedule'] = ScheduleSerializer(schedule_object).data
                response['booked_seats'] = booked_seats
            return JsonResponse(response)
        except (KeyError, json.decoder.JSONDecodeError, ScheduledVehicle.DoesNotExist, Schedule.DoesNotExist) as exp:
            return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    else:
        sv_objects = ScheduledVehicle.objects.all()
        for sv_object in sv_objects:
            data = ScheduledVehicleSerializer(sv_object).data
            data['vehicle']['vehicleType']['layout'] = None
            response.append(data)
        return JsonResponse({'scheduledVehicles': response})


def search(request):
    '''
    View for handling search, takes in request and gives out list of SchudeledVehicles
    {
        "route":1,
        "date":"2019-11-16T08:15:00.000"
    }
    '''
    if request.method == "POST":
        response = []
        try:
            request_json = json.loads(request.body.decode('utf-8'))
            route = Route.objects.get(id=int(request_json['route']))
            schedules = Schedule.objects.filter(date=datetime_str_to_object(request_json['date']).date(), route=route)
            for schedule_object in schedules:
                schedule_data = ScheduleSerializer(schedule_object).data
                s_vehicles = schedule_object.scheduledvehicle_set.all()
                for s_vehicle in s_vehicles:
                    data = ScheduledVehicleSerializer(s_vehicle).data
                    data['vehicle']['vehicleType']['layout'] = None
                    data['schedule'] = schedule_data
                    response.append(data)
            return JsonResponse({'scheduledVehicles':response})
        except (KeyError, json.decoder.JSONDecodeError, Route.DoesNotExist, Schedule.DoesNotExist) as exp:
            return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    return JsonResponse({'sd':'sd'})


def book(request, booked_uuid):
    '''
    Views for handling booking action
    {
        "trip":1,
        "schedule":3,
        "seat": "A7",
        "bookedBy": "6e6a4570-71e1-40bb-a6f7-e5261aae2634",
        "passengerName":"Some name",
        "passengerPhone":984654131,
        "amount":5000,
        "isPaid":True,
        "paymentMethod": "Khalti",
        "bookedOn":"2019-11-16T18:15:00.000"
    }
    '''
    if request.method == "POST":
        try:
            request_json = json.loads(request.body.decode('utf-8'))
            trip = ScheduledVehicle.objects.get(id=int(request_json['trip']))
            seat = Seat.objects.get(layout=trip.vehicle.vehicle_type.layout, label=str(request_json['seat']))
            schedule_object = Schedule.objects.get(id=int(request_json['schedule']))
            user = CustomUserBase.objects.get(unique_id=str(request_json['bookedBy']))
            if int(user.id) != int(request.user.id):
                return JsonResponse({'status':False, 'error':"Intrusion Detected!"})
            if str(user.user_type)=="Agent":
                pass # do something with the credits later
            try:
                booked = Booking.objects.get(trip=trip, seat=seat, schedule=schedule_object)
                if booked:
                    return JsonResponse({'status':False, 'error':"This Seat is already booked by someone else."})
            except Booking.DoesNotExist:
                booked = Booking.objects.create(trip=trip,
                                                schedule=schedule_object,
                                                seat=seat,
                                                booked_by=user,
                                                passenger_name=str(request_json['passengerName']),
                                                passenger_phone=int(request_json['passengerPhone']),
                                                amount=int(request_json['amount']),
                                                is_paid=request_json['isPaid'],
                                                payment_method=str(request_json['paymentMethod']),
                                                booked_on=datetime_str_to_object(request_json['bookedOn'])
                                                )
                booked.save()
                return JsonResponse({'bookedingId':int(booked.id)})
        except (KeyError, json.decoder.JSONDecodeError, ScheduledVehicle.DoesNotExist, Seat.DoesNotExist) as exp:
            return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})

    return JsonResponse({'error':'Still in progress aaba ekxin paxi garxu'})
    # response = []
    # if booked_uuid:
    #     pass
    
    # user