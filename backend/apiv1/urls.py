from django.urls import path, include
from . import views
from config.views import CustomTokenObtainPairView, logout_view
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'profile', views.StudentProfileDetailView, basename='student-profile')


urlpatterns = [

    path('', include(router.urls)),

    path('search', views.student_search, name='student-search'),


    path('register', views.StudentRegistrationView.as_view(), name='student-register'),
    path('login', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout', logout_view, name='logout'),


    
]