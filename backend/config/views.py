from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from rest_framework import viewsets, permissions, status, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied  
from django.shortcuts import redirect



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        client_ip = self._get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        username = request.data.get('username')

        response = super().post(request, *args, **kwargs)

        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip



def logout_view(request):

    logout(request)

    access_token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[-1]
    if access_token:
        from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
        try:
            token = OutstandingToken.objects.get(token=access_token)
            BlacklistedToken.objects.get_or_create(token=token)
        except OutstandingToken.DoesNotExist:
            pass

    return redirect('login')

