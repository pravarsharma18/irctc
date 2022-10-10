from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from base.choices import Constants

from .models import Train
from .permissions import CreatePermission
from .serializers import TrainSerializer
from .filters import TrainFilters
from datetime import datetime, timedelta


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
