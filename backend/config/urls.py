from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('apiv1.urls')),
    path('student/', include('student.urls')),

    
    path('login', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),

    path('auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


