import django_filters
from django_filters import rest_framework as filters

from django.db.models import Count, Value

from .models import Train


class TrainFilters(filters.FilterSet):
    class Meta:
        model = Train
        distinct = True
        fields = {
            'name': ['icontains'],
            'number': ['exact'],
        }
