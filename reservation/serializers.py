from rest_framework import serializers

from .models import PassengerDetail, Reservation, UserJourney, ReservationChartForTrain, WaitingList
from datetime import datetime, timedelta
from base.choices import Constants, JourneyStatus
from django.db import transaction


class PassengerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerDetail
        fields = ['id', 'first_name', 'last_name',
                  'age', 'gender', 'birth_preference']


class UserJourneySerializer(serializers.ModelSerializer):
    passengers = serializers.PrimaryKeyRelatedField(queryset=PassengerDetail.objects.all(),
                                                    many=True, write_only=True)
    user = serializers.StringRelatedField(source="user.email")
    status = serializers.StringRelatedField(read_only=True)
    passengers_list = serializers.SerializerMethodField()

    def get_passengers_list(self, obj):
        return PassengerDetailSerializer(obj.passengers.all(), many=True).data

    @transaction.atomic
    def create(self, validated_data):
        print("validated_datavalidated_data", validated_data)
        max_date = datetime.now().date() + timedelta(days=Constants.BOOKING_FOR_NEXT_DAYS)
        if validated_data['date'] > max_date:
            raise serializers.ValidationError(
                {"detail": f"Can only book a Train for next {Constants.BOOKING_FOR_NEXT_DAYS} days."})

        reservation_qs = ReservationChartForTrain.objects.filter(
            date=validated_data['date'], train=validated_data['train'])
        if not reservation_qs.exists():
            raise serializers.ValidationError(
                {"detail": f"{validated_data['train'].name} numbered {validated_data['train'].number} \
                            does not runs on {validated_data['date'].strftime('%A')}"})
        else:
            reservation_obj = reservation_qs.first()
            new_journey = UserJourney(**validated_data)
            new_journey.save()
            if reservation_obj.vacant_seats > 0:
                passengers_data = validated_data.pop('passengers')
                validated_data['status'] = JourneyStatus.CONFIRMED.name

                validated_data['user'] = self.context['request'].user

                for passenger in passengers_data:
                    new_journey.passengers.add(passenger)
                    reservation_obj.vacant_seats -= 1
                reservation_obj.user_journey.add(new_journey)
                reservation_obj.save()
            else:
                validated_data['status'] = JourneyStatus.WAITING.name
                # waiting list logic
                # WaitingList.objects.create()

        return new_journey

    class Meta:
        model = UserJourney
        fields = ['id', 'date', 'user', 'status', 'passengers',
                  'train', 'source_station', 'destination_station', 'passengers_list']


class ReservationSerializer(serializers.ModelSerializer):
    # passenger_detail = serializers.PrimaryKeyRelatedField(queryset=PassengerDetail.objects.all(),
    #                                                       many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user_journey']
        depth = True


class ReservationChartForTrainSerializer(serializers.ModelSerializer):
    train = serializers.SerializerMethodField()
    # vacant_seats = serializers.IntegerField(read_only=True)
    # total_seats = serializers.IntegerField(read_only=True)
    passengers = serializers.SerializerMethodField()

    # def get_user_journey(self, obj):
    #     print(obj.user_journey.all())
    #     return obj.user_journey.all()

    def get_train(self, obj):
        return {
            "name": obj.train.name,
            "number": obj.train.number
        }

    def get_passengers(sel, obj):
        return UserJourneySerializer(obj.user_journey.all(), many=True).data
        print("*"*50)
        print(a)
        print("*"*50)

        return {
            "passengers": PassengerDetailSerializer(a.user_journey.all(), many=True).data
        }

    def create(self, validated_data):
        print(validated_data)
        chart_obj = ReservationChartForTrain.objects.filter(
            train=validated_data['train'])
        print("chart_obj", chart_obj)
        if chart_obj.exists():
            raise serializers.ValidationError(
                {"detail": "Chart Already Exists."})
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    class Meta:
        model = ReservationChartForTrain
        fields = ['id', 'train', 'date', 'total_seats',
                  'vacant_seats', 'passengers']
