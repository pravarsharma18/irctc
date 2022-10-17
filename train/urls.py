from django.urls import path, include
from rest_framework import routers

from .views import TrainViewSet

router = routers.SimpleRouter()

router.register(r'train', TrainViewSet)

urlpatterns = [
    path('reservations/', include('reservation.urls')),
    path("users/", include('users.urls')),
]
urlpatterns += router.urls
