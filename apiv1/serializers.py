''' Searializers module for models of api '''

from rest_framework import serializers

from .models import VehicleItem, SeatItem, Route, Vehicle, VehicleType
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
    routes = RouteSerializer(many=True)
    vehicleType = VehicleTypeSerializer(source='vehicle_type')
    numberPlate = serializers.CharField(source='number_plate')

    class Meta:
        model = Vehicle
        fields = ['id', 'vehicleType', 'routes', 'numberPlate']


class SeatItemSerializer(serializers.ModelSerializer):
    ''' Serializer class for SeatItemSerializer model '''
    class Meta:
        model = SeatItem
        fields = ['label', 'state', 'booking_details']


class VehicleItemSerializer(serializers.ModelSerializer):
    ''' Serializer class for VehicleItemSerializer model '''
    seat_items = SeatItemSerializer(many=True)
    route = RouteSerializer()
    vehicle = VehicleSerializer()

    class Meta:
        model = VehicleItem
        fields = '__all__'
