from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('', SomethingViewSet, basename='user')

urlpatterns = [
    path('user/', include(router.urls)),
]