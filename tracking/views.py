import datetime
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import BasePermission
from tracking import models,serializers
from users.models import CustomerProfile, DriverProfile

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.user_type == 2:
            return request.user == obj.customer.user
        return request.user == obj.driver.user


class TrackingModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsOwner]
    serializer_class = serializers.TrackingSerializer
    http_method_names = ['get','put']

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 2:
            return models.Tracking.objects.filter(customer__user=user)
        return models.Tracking.objects.filter(driver__user=user)


class RequestModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsOwner]
    serializer_class = serializers.RequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 2:
            return models.Request.objects.filter(customer__user=user)
        return models.Request.objects.filter(is_accepted=False)

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type == 2:
            customer = CustomerProfile.objects.get(user=user)
            serializer.save(customer=customer)
        serializer.save()



class AcceptRequestAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            user = request.user
            if user.user_type == 2:
                return Response({'msg':"you are not a driver."},status=status.HTTP_201_CREATED)
            ride_request = models.Request.objects.get(id=request.data['request_id'])
            if ride_request.is_accepted:
                return Response({'msg':"Already accepted."},status=status.HTTP_201_CREATED)
            driver_profile = DriverProfile.objects.get(user=user)
            if models.Tracking.objects.filter(driver=driver_profile,is_completed=False).exists():
                return Response({'msg':"Please complete your ride first."},status=status.HTTP_201_CREATED)
            ride_request.driver = driver_profile
            ride_request.driver.is_accepted=True
            ride_request.save()
            models.Tracking.objects.create(
                customer=ride_request.customer,
                driver = driver_profile,
                driver_longitude=request.data['driver_longitude'],
                driver_latitude = request.data['driver_latitude'],
                request = ride_request
            )
            return Response({'msg':"Ride is accepted."},status=status.HTTP_201_CREATED) 
        except Exception as e:
            print(e)
            return Response({'error':e},status=status.HTTP_400_BAD_REQUEST)

class EndRequestAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            user = request.user
            ride_request = models.Request.objects.get(id=request.data['request_id'])
            tracking = models.Tracking.objects.get(request=ride_request)
            tracking.ended_at = datetime.datetime.now()
            tracking.is_completed=True
            if user.user_type == 2:
                tracking.ended_by = 2
            else:
                tracking.ended_by = 3
            tracking.save()
            return Response({'msg':"Ride is ended."},status=status.HTTP_201_CREATED) 
        except Exception as e:
            print(e)
            return Response({'error':e},status=status.HTTP_400_BAD_REQUEST)