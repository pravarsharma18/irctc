from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from train.models import Berth

from .models import PassengerDetail, Reservation, Ticket, ReservationChartForTrain, WaitingList
from datetime import datetime, timedelta
from base.choices import BerthPreference, BoggyName, Coaches, Constants, JourneyStatus
from django.db import transaction


class PassengerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerDetail
        fields = ['id', 'first_name', 'last_name',
                  'age', 'gender', 'quota', 'berth_preference']

    def validate(self, attrs):
        if attrs['quota'] == Coaches.AC1.name:
            if attrs['berth_preference'] in [BerthPreference.MIDDLE.name,
                                             BerthPreference.SIDE_LOWER.name,
                                             BerthPreference.SIDE_UPPER.name]:
                raise ValidationError(
                    {"detail": f"{attrs['quota']} doest not have {attrs['berth_preference']} berth."})

        if attrs['quota'] == Coaches.AC2.name:
            if attrs['berth_preference'] in [BerthPreference.MIDDLE.name]:
                raise ValidationError(
                    {"detail": f"{attrs['quota']} doest not have {attrs['berth_preference']} berth."})
        return attrs


class TicketSerializer(serializers.ModelSerializer):
    passengers = serializers.PrimaryKeyRelatedField(queryset=PassengerDetail.objects.all(),
                                                    many=True, write_only=True)
    user = serializers.StringRelatedField(source="user.email")
    status = serializers.StringRelatedField(read_only=True)
    passengers_list = serializers.SerializerMethodField()
    pnr = serializers.StringRelatedField(read_only=True)
    # source_station = serializers.CharField(source='source_station.name')
    # destination_station = serializers.CharField(
    #     source='destination_station.name')
    # train = serializers.CharField(source='train.name')

    def get_passengers_list(self, obj):
        return PassengerDetailSerializer(obj.passengers.all(), many=True).data

    @transaction.atomic
    def create(self, validated_data):
        date = validated_data['date']
        train = validated_data['train']
        passengers = validated_data['passengers']
        # print("validated_datavalidated_data", validated_data)
        max_date = datetime.now().date() + timedelta(days=Constants.BOOKING_FOR_NEXT_DAYS)
        if date > max_date:
            raise serializers.ValidationError(
                {"detail": f"Can only book a Train for next {Constants.BOOKING_FOR_NEXT_DAYS} days."})
        if len(passengers) <= 0:
            raise serializers.ValidationError(
                {"detail": "Must have valid passengers"})
        reservation_qs = ReservationChartForTrain.objects.filter(
            date=date, train=train)
        if not reservation_qs.exists():
            raise serializers.ValidationError(
                {"detail": f"{train.name} numbered {train.number} does not runs on {date.strftime('%A')}"})
        else:
            reservation_obj = reservation_qs.first()
            if reservation_obj.vacant_seats > 0:
                passengers_data = validated_data.pop('passengers')
                validated_data['status'] = JourneyStatus.CONFIRMED.name

                validated_data['user'] = self.context['request'].user

                new_journey = Ticket(**validated_data)
                new_journey.save()

                for passenger in passengers_data:
                    berth = passenger.berth_preference
                    quota = passenger.quota

                    berth_obj = Berth.objects.filter(
                        date=date, train__number=train.number)
                    fields = {
                        'name__icontains': getattr(BoggyName, '%s' % quota).value,
                        f'{berth.lower()}__gt': 0,
                    }
                    berth_obj = berth_obj.filter(
                        **fields).first()

                    setattr(berth_obj, berth.lower(), int(
                        getattr(berth_obj, berth.lower()) - 1))
                    berth_obj.save()
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
        model = Ticket
        fields = ['id', 'pnr', 'date', 'user', 'status', 'passengers',
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
    tickets = serializers.SerializerMethodField()

    # def get_user_journey(self, obj):
    #     print(obj.user_journey.all())
    #     return obj.user_journey.all()

    def get_train(self, obj):
        return {
            "name": obj.train.name,
            "number": obj.train.number
        }

    def get_tickets(sel, obj):
        data = []
        for user_j in obj.user_journey.all():
            data.append({
                'id': user_j.id,
                'pnr': user_j.pnr,
                'user': user_j.user.email,
                'status': user_j.status,
                'from': user_j.source_station.name,
                'to': user_j.destination_station.name,
                'passengers': [{'first_name': passenger.first_name, 'last_name': passenger.last_name,
                               'age': passenger.age, 'gender': passenger.gender, 'berth': passenger.berth_preference} for passenger in user_j.passengers.all()]

            })
        # return UserJourneySerializer(obj.user_journey.all(), many=True).data
        return data

    def create(self, validated_data):
        chart_obj = ReservationChartForTrain.objects.filter(
            train=validated_data['train'])
        if chart_obj.exists():
            raise serializers.ValidationError(
                {"detail": "Chart Already Exists."})
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    class Meta:
        model = ReservationChartForTrain
        fields = ['id', 'train', 'date', 'total_seats',
                  'vacant_seats', 'tickets']
