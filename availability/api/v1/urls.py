from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .viewsets import *

router = DefaultRouter()
router.register("availability", AvailabilityViewSet, "availability")

app_name = "availability"

urlpatterns = [
    path("", include(router.urls)),
]