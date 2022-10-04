import django_filters
from django_filters import rest_framework as filters

from django.db.models import Count, Value

from .models import Train


class TrainFilters(filters.FilterSet):
    train_by_number = django_filters.CharFilter(method='filter_train_by_number', field_name='train_number')
    
    def filter_train_by_number(self, queryset, name, values):
        total_count = queryset.filter(train_number=values).aggregate(total_routes=Count('train_number'))
        queryset = queryset.annotate(total_routes=Value(total_count['total_routes']))[:1]
        return queryset

    class Meta:
        model = Train
        distinct = True
        fields = {
            # 'name':['icontains'],
            # 'train_number': ['icontains'],
            # 'station_code': ['icontains'],
            'station_name':['icontains'],
            'source_station':['icontains'],
            # 'source_short_name':['icontains'],
            # 'type':['exact'],
        }
