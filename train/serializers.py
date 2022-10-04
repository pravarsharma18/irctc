from rest_framework import serializers
from .models import Train


class TrainSerializer(serializers.ModelSerializer):
        class Meta:
            model = Train
            fields = ['id','train_number', 'name', 'station_name', 'station_code', 'source_station', 'source_short_name',
                    'arrival_time', 'departure_time', 'destination_station', 'destination_short_name', 'distance',
                    'sequence', 'type', 'runs_on']


class TrainDetailSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()


    class Meta:
        model = Train
        fields = ['details']