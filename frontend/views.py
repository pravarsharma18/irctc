from django.shortcuts import render, redirect

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

# Create your views here.


class DashboardListView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        context = {
            'dashboard': True,
            'name': 'Dashboard'
        }
        return render(request, 'frontend/dashboard.html', context)


class BookingView(LoginRequiredMixin, View):

    @staticmethod
    def get(request, *args, **kwargs):
        context = {
            'dashboard': True,
            'name': 'Booking',
            'url': settings.MAIN_URL
        }
        return render(request, 'frontend/booking.html', context)


class SignInView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        print(request.GET, args, kwargs)
        # if request.GET.get('next'):
        #     return redirect(request.GET.get('next'))
        return render(request, 'frontend/signin.html')


class SignUpView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        print(request.GET, args, kwargs)
        return render(request, 'frontend/signup.html')
