import django_filters
from django_filters import rest_framework as filters

from django.db.models import Count, Value, Q, F, OuterRef, Subquery


from .models import Train, Station, TrainWithStations


class TrainFilters(filters.FilterSet):
    def filter_stations(queryset, name, value):
        print("source***************", queryset, name, value)
        if not value:
            return queryset
        source = ""
        destination = ""
        try:
            source = value.split(',')[0]
            destination = value.split(',')[1]
        except:
            pass

        train_queryset = queryset.filter(
            Q(station__name__icontains=source.strip()) and Q(
                station__name__icontains=destination.strip())
        )

        if train_queryset.exists():
            return train_queryset
        return queryset

    source_station = filters.CharFilter(
        field_name='stations', method=filter_stations)

    class Meta:
        model = Train
        distinct = True
        fields = {
            'name': ['icontains'],
            'number': ['exact'],
        }
