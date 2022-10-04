from django.urls import path, include
from rest_framework import routers

from .views import TrainViewSet, get_search, TrainSchedule

router = routers.SimpleRouter()

router.register(r'train', TrainViewSet)

urlpatterns = [
    path('search/',get_search),
    path('train_details/<int:train_number>/', TrainSchedule.as_view()),
    path('reservations/', include('reservation.urls')),
]
urlpatterns += router.urls
