from rest_framework import serializers
from .models import Train, Station, TrainWithStations, State, City


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    display_state = serializers.StringRelatedField(source='state.name')
    state = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(), write_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'display_state', 'state']


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'


class TrainWithStationsSerializer(serializers.ModelSerializer):

    station = serializers.StringRelatedField(source="station.name")

    class Meta:
        model = TrainWithStations
        fields = ['station', 'sequence', 'distance',
                  'base_fare', 'arrival', 'departure']


class TrainSerializer(serializers.ModelSerializer):
    station = serializers.PrimaryKeyRelatedField(
        queryset=Station.objects.all(), many=True, write_only=True)
    stations = serializers.SerializerMethodField()

    def get_stations(self, obj):
        stations = TrainWithStations.objects.filter(train=obj)
        serializer = TrainWithStationsSerializer(stations, many=True).data
        return serializer

    class Meta:
        model = Train
        fields = ['id', 'number', 'name', 'station',
                  'stations', 'type', 'runs_on']


class TrainDetailSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = Train
        fields = ['details']
