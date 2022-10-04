from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Train
from .permissions import CreatePermission
from .serializers import TrainSerializer, TrainDetailSerializer
from .filters import  TrainFilters


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TrainFilters
    search_fields = ['name', 'train_number', 'station_name', 'station_code','destination_station', 'destination_short_name']
    distinct = True
    permission_classes = [CreatePermission]


class TrainDetails(generics.RetrieveAPIView):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    lookup_field = 'train_number'

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(train_number=kwargs['train_number'])
        if not queryset.exists():
            return Response({"detail":"Train not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_search(request):
    return render(request, 'train/index.html', {})
