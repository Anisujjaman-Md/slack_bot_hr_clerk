from django.urls import path, include
from rest_framework import routers
from bot_app.views import BotViewSet, BotFormViewSet

router = routers.DefaultRouter()
router.register('', BotViewSet, basename='slack-bot')
router.register('form', BotFormViewSet, basename='form')

urlpatterns = [
    path('slack-bot/', include(router.urls)),
]

