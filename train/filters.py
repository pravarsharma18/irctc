from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as filters

from .models import Train, TrainWithStations
from datetime import datetime, timedelta
from base.choices import Constants
from django.db.models import Q


class TrainFilters(filters.FilterSet):
    def source_station(queryset, name, value):
        if not value:
            return queryset

        train_queryset = queryset.filter(
            Q(station__name__icontains=value) |
            Q(station__short_name__icontains=value)
        )

        if train_queryset.exists():
            return train_queryset

        return train_queryset

    def destination_station(queryset, name, value):
        train_qs = TrainWithStations.objects.filter(
            Q(station__city__name__icontains=value) |
            Q(station__short_name__icontains=value)
        ).order_by('-sequence')
        if train_qs.exists():
            final_train = train_qs[0]
            return queryset.filter(number=final_train.train.number)

        return train_qs

    def date(queryset, name, value):
        if value > (datetime.now().date() + timedelta(days=Constants.BOOKING_FOR_NEXT_DAYS)):
            raise ValidationError(
                {"detail": f"Can't book a train more than {Constants.BOOKING_FOR_NEXT_DAYS} days."})
        return queryset
    source_station = filters.CharFilter(
        field_name='source_station', method=source_station)

    destination_station = filters.CharFilter(
        field_name='destination_station', method=destination_station)

    date = filters.DateFilter(
        field_name='date', method=date)

    class Meta:
        model = Train
        distinct = True
        fields = {
            'name': ['icontains'],
            'number': ['exact'],
        }
