from django.urls import path, include
from rest_framework import routers

from .views import TrainViewSet, StateViewSet, CityViewSet

router = routers.SimpleRouter()

router.register(r'train', TrainViewSet)
router.register(r'state', StateViewSet)
router.register(r'city', CityViewSet)

urlpatterns = [
    path('reservations/', include('reservation.urls')),
    path("users/", include('users.urls')),
]
urlpatterns += router.urls
