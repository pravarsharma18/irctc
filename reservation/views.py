from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


from .filters import ReservationChartFilters
from .models import PassengerDetail, Reservation, Ticket, ReservationChartForTrain
from .serializers import (PassengerDetailSerializer, ReservationSerializer,
                          ReservationChartForTrainSerializer, TicketSerializer)


class PassengerDetailViewSet(viewsets.ModelViewSet):
    queryset = PassengerDetail.objects.all()
    serializer_class = PassengerDetailSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class ReservationChartForTrainViewSet(viewsets.ModelViewSet):
    queryset = ReservationChartForTrain.objects.all()
    serializer_class = ReservationChartForTrainSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ReservationChartFilters
    search_fields = ['name', 'number', 'station__name']
