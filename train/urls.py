from django.urls import path, include
from rest_framework import routers

from .views import TrainViewSet

router = routers.SimpleRouter()

router.register(r'train', TrainViewSet)

urlpatterns = [
    path('reservations/', include('reservation.urls')),
]
urlpatterns += router.urls
