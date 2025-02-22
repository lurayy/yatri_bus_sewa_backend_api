''' Searializers module for models of api '''
from rest_framework import serializers
from .models import VehicleType, Route, Vehicle, Schedule, ScheduledVehicle
from .utils import layout_to_json


class VehicleTypeSerializer(serializers.ModelSerializer):
    ''' Serializer class for VehicleType model '''
    layout = serializers.SerializerMethodField()

    class Meta:
        model = VehicleType
        fields = '__all__'

    def get_layout(self, obj):
        ''' Serializer function for layout field '''
        return layout_to_json(obj.layout)


class RouteSerializer(serializers.ModelSerializer):
    ''' Serializer class for RouteSerializer model '''
    class Meta:
        model = Route
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    ''' Serializer class for VehicleSerializer model '''
    vehicleType = VehicleTypeSerializer(source='vehicle_type')
    numberPlate = serializers.CharField(source='number_plate')

    class Meta:
        model = Vehicle
        fields = ['id', 'vehicleType', 'numberPlate']


class ScheduleSerializer(serializers.ModelSerializer):
    ''' Serializere class for Schedule Model'''
    route = RouteSerializer()

    class Meta:
        model = Schedule
        fields = '__all__'

class ScheduledVehicleSerializer(serializers.ModelSerializer):
    ''' Serializere class for ScheduledVehicle Model '''
    vehicle = VehicleSerializer()
    schedule = ScheduleSerializer(many=True)

    class Meta:
        model = ScheduledVehicle
        fields = '__all__'
