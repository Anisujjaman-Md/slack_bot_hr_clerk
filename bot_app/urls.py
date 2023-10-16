from django.urls import path, include
from rest_framework import routers
from bot_app import views
from bot_app.views import BotViewSet

router = routers.DefaultRouter()
router.register('', BotViewSet, basename='slack-bot')

urlpatterns = [
    path('slack-bot/', include(router.urls)),
    path('slack-interaction/', views.slack_interaction, name='slack-interaction'),
]

