from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import *

router = DefaultRouter()
router.register('schedule-ride', ScheduleRideViewSet, basename='schedule_ride')

app_name = "schedule_ride"

urlpatterns = [
    path('', include(router.urls))
]
