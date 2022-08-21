from django.utils.translation import ugettext_lazy as _ 
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import CustomerProfile, DriverProfile
from .serializers import *


class ScheduleRideViewSet(ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post', 'get', 'put']
    serializer_class = ScheduleRideSerializer
    queryset = ScheduleRide.objects.none()

    def get_serializer_class(self):
        if self.action == 'update':
            return CancelScheduleRideSerializer
        return ScheduleRideSerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 2:
            return ScheduleRide.objects.filter(customer__user=user, is_canceled=False, is_active=True) # upcomming rides
        elif user.user_type == 3:
            return ScheduleRide.objects.filter(driver__user=user, is_canceled=False, is_active=True) # new rides
        return ScheduleRide.objects.filter(is_canceled=False)

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type == 2:
            customer = CustomerProfile.objects.get(user=user)
            serializer.save(customer=customer)
        serializer.save()
