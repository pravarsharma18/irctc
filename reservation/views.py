from django.shortcuts import render
from rest_framework import viewsets

from .models import PassengerDetail, Reservation, UserJourney, ReservationChartForTrain
from .serializers import (PassengerDetailSerializer, ReservationSerializer,
                         ReservationChartForTrainSerializer, UserJourneySerializer)



class PassengerDetailViewSet(viewsets.ModelViewSet):
    queryset = PassengerDetail.objects.all()
    serializer_class = PassengerDetailSerializer
    

class UserJourneyViewSet(viewsets.ModelViewSet):
    queryset = UserJourney.objects.all()
    serializer_class = UserJourneySerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    
class ReservationChartForTrainViewSet(viewsets.ModelViewSet):
    queryset = ReservationChartForTrain.objects.all()
    serializer_class = ReservationChartForTrainSerializer
