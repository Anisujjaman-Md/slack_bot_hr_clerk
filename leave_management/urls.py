from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('', SomethingViewSet, basename='leave')

urlpatterns = [
    path('leave/', include(router.urls)),
]