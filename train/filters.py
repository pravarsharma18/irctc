from django_filters import rest_framework as filters

from .models import Train, TrainWithStations


class TrainFilters(filters.FilterSet):
    def source_station(queryset, name, value):
        if not value:
            return queryset

        train_queryset = queryset.filter(station__name__icontains=value)

        if train_queryset.exists():
            return train_queryset

        return train_queryset

    def destination_station(queryset, name, value):

        train_qs = TrainWithStations.objects.filter(
            station__city__name__icontains=value).order_by('-sequence')
        if train_qs.exists():
            final_train = train_qs[0]
            return queryset.filter(number=final_train.train.number)

        return train_qs

    source_station = filters.CharFilter(
        field_name='source_station', method=source_station)

    destination_station = filters.CharFilter(
        field_name='destination_station', method=destination_station)

    class Meta:
        model = Train
        distinct = True
        fields = {
            # 'name': ['icontains'],
            # 'number': ['exact'],
        }
