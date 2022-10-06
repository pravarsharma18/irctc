from rest_framework import serializers
from .models import Train, Station, TrainWithStations


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'


class TrainWithStationsSerializer(serializers.ModelSerializer):

    station = serializers.StringRelatedField(source="station.name")

    class Meta:
        model = TrainWithStations
        fields = ['station', 'sequence', 'distance', 'base_fare']


class TrainSerializer(serializers.ModelSerializer):
    station = serializers.PrimaryKeyRelatedField(
        queryset=Station.objects.all(), many=True, write_only=True)
    stations = serializers.SerializerMethodField()

    def get_stations(self, obj):
        t = TrainWithStations.objects.filter(train=obj)
        ser = TrainWithStationsSerializer(t, many=True).data
        return ser

    class Meta:
        model = Train
        fields = ['id', 'number', 'name', 'station',
                  'stations', 'type', 'runs_on']


class TrainDetailSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = Train
        fields = ['details']
