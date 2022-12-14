from datetime import datetime, timedelta
from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Train, State, City
from .permissions import CreatePermission
from .serializers import TrainSerializer, StateSerializer, CitySerializer
from .filters import TrainFilters, CityFilters, StateFilters


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StateFilters


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CityFilters


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TrainFilters
    search_fields = ['name', 'number', 'station__name']
    permission_classes = [CreatePermission]
    lookup_field = 'number'


def get_search(request):
    return render(request, 'train/index.html', {})
