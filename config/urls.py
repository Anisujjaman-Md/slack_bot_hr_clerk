from django.contrib import admin
from django.urls import path, include
from .views import ServerStatus
urlpatterns = [
    path('test/', ServerStatus.as_view(), name='server-status'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('bot_app.urls')),
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('leave_management.urls')),
]