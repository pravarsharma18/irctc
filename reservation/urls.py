from django.urls import path
from rest_framework import routers

from .views import (PassengerDetailViewSet, ReservationViewSet, 
                    UserJourneyViewSet, ReservationChartForTrainViewSet
                    )


router = routers.SimpleRouter()

router.register(r'chartfortrain', ReservationChartForTrainViewSet, basename='reservation')
router.register(r'passanger', PassengerDetailViewSet)
router.register(r'reservation', ReservationViewSet)
router.register(r'journey', UserJourneyViewSet)

urlpatterns = router.urls
