from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import get_tokens_for_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer

# Create your views here.

User = get_user_model()


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = []


class LoginView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        try:
            print(request.data)
            user = authenticate(request, username=request.data['username'], password=request.data['password'])
            print("USER: ",user)
            if not user:
                return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({**auth_data}, status=status.HTTP_200_OK)
        except KeyError as e:
            return Response({'detail': f'Key {e} is required'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        logout(request)
        return Response({'detail': 'Successfully Logged out'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def post(request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)  # Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_200_OK)
