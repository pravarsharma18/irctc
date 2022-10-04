from django.urls import path
from .views import UserRegistrationView, LoginView, LogoutView,ChangePasswordView
from rest_framework_simplejwt import views as jwt_views

app_name = 'users'

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]