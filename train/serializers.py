from rest_framework import serializers
from .models import Train


class TrainSerializer(serializers.ModelSerializer):
    runs_on = serializers.SerializerMethodField()
    
    def get_runs_on(self, obj):
        return [ i[0] for i in obj.runs_on]

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