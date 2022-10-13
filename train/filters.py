from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as filters

from reservation.models import ReservationChartForTrain

from .utils import sequence_filter

from .models import Train, TrainWithStations
from datetime import datetime, timedelta
from base.choices import Constants
from django.db.models import Q
from pprint import pprint


class TrainFilters(filters.FilterSet):
    def stations(queryset, name, value):
        if not value:
            return queryset
        source = ""
        destination = ""
        try:
            source = value.split(',')[0]
            destination = value.split(',')[1]
        except:
            raise ValidationError(
                {"detail": "Please enter source as well as destination."})

        source_queryset = TrainWithStations.objects.filter(
            Q(station__name__icontains=source.strip())
        )
        destination_queryset = TrainWithStations.objects.filter(
            Q(station__name__icontains=destination.strip())
        )

        if not source_queryset or not destination_queryset:
            raise ValidationError({"detail": "No Trains found"})

        seq_index, source_list = sequence_filter(
            source_queryset, destination_queryset)

        new_queryset = TrainWithStations.objects.filter(
            sequence=source_list[seq_index], station__name__icontains=source.strip())

        if new_queryset.exists():
            t_number = []
            for i in new_queryset:
                t_number.append(i.train.number)
            return queryset.filter(number__in=t_number)

        return source_queryset

    def date(queryset, name, value):
        if value > (datetime.now().date() + timedelta(days=Constants.BOOKING_FOR_NEXT_DAYS)):
            raise ValidationError(
                {"detail": f"Can't book a train more than {Constants.BOOKING_FOR_NEXT_DAYS} days."})
        """
            Logic to get the next and previous date trains
        
            previous_dates = [value - timedelta(days) for days in range(1, 6)]
            next_dates = [value + timedelta(days) for days in range(1, 6)]

            previous_trains_qs = ReservationChartForTrain.objects.filter(
                train__in=queryset, date__in=previous_dates)

            next_train_qs = ReservationChartForTrain.objects.filter(
                train__in=queryset, date__in=next_dates)

            final_qs = []
            for i in [t.reservation_charts.filter(Q(date__in=previous_dates) | Q(date__in=next_dates)) for t in queryset]:
                for a in i:
                    final_qs.append({
                        "name": a.train.name,
                        "number": a.train.number,
                        "runs_on": a.train.runs_on
                    })
                    # print("t", data)

            a = Train.objects.none()
            a |= final_qs
        """
        return queryset

    station = filters.CharFilter(
        field_name='source_station', method=stations)

    # source_station = filters.CharFilter(
    #     field_name='source_station', method=source_station)

    # destination_station = filters.CharFilter(
    #     field_name='destination_station', method=destination_station)

    date = filters.DateFilter(
        field_name='date', method=date)

    class Meta:
        model = Train
        distinct = True
        fields = {
            'name': ['icontains'],
            'number': ['exact'],
        }
