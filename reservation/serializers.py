from imp import source_from_cache
from rest_framework import serializers

from .models import PassengerDetail, Reservation, UserJourney, ReservationChartForTrain



class PassengerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerDetail
        fields = ['id','first_name', 'last_name', 'age', 'gender', 'birth_preference']


class UserJourneySerializer(serializers.ModelSerializer):
    passengers = serializers.PrimaryKeyRelatedField(queryset=PassengerDetail.objects.all(), \
                                                    many=True)

    class Meta:
        model = UserJourney
        fields = ['id', 'user', 'passengers', 'train', 'source_station', 'destination_station']


class ReservationSerializer(serializers.ModelSerializer):
    passenger_detail = serializers.PrimaryKeyRelatedField(queryset=PassengerDetail.objects.all(), \
                                                          many=True)
    class Meta:
        model = Reservation
        fields = ['id', 'passenger_detail', 'user_journey']

class ReservationChartForTrainSerializer(serializers.ModelSerializer):
    # vacant_seats = serializers.IntegerField(read_only=True)
    # total_seats = serializers.IntegerField(read_only=True)
    # user_journey = serializers.PrimaryKeyRelatedField(queryset=UserJourney.objects.all())

    # def get_user_journey(self, obj):
    #     print(obj.user_journey.all())
    #     return obj.user_journey.all()

    def create(self, validated_data):
        print(validated_data)
        chart_obj = ReservationChartForTrain.objects.filter(train=validated_data['train'])
        print("chart_obj",chart_obj)
        if chart_obj.exists():
            raise serializers.ValidationError({"detail":"Chart Already Exists."})
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    class Meta:
        model = ReservationChartForTrain
        fields = ['id', 'train', 'vacant_seats', 'total_seats', 'user_journey']