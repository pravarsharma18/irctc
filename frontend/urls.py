from django.urls import path
from .views import DashboardListView, SignInView, SignUpView, BookingView

app_name = "frontend"

urlpatterns = [
    path("", DashboardListView.as_view(), name='dashboard'),
    path("booking/", BookingView.as_view(), name='booking'),
    path("signin/", SignInView.as_view(), name='signin'),
    path("signup/", SignUpView.as_view(), name='signup'),
    # path("logout/"),
]