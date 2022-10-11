from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as filters

from .models import ReservationChartForTrain
from datetime import datetime, timedelta
from base.choices import Constants
from django.db.models import Q


class ReservationChartFilters(filters.FilterSet):
    class Meta:
        model = ReservationChartForTrain
        distinct = True
        fields = {
            'train__name': ['icontains'],
            'train__number': ['icontains'],
            'date': ['exact']
        }
