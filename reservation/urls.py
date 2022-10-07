from django.urls import path
from rest_framework import routers

from .views import (PassengerDetailViewSet, UserJourneyViewSet,
                    ReservationChartForTrainViewSet
                    )


router = routers.SimpleRouter()

router.register(r'chartfortrain',
                ReservationChartForTrainViewSet, basename='reservation')  # Added using celery tasks. on daily basis.
router.register(r'passanger', PassengerDetailViewSet)
router.register(r'journey', UserJourneyViewSet)

urlpatterns = router.urls
