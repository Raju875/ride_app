from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from datetime import datetime, date

from availability.models import *
from .serializers import *


class AvailabilityViewSet(ViewSet):
    authentication_class = [authentication.TokenAuthentication]
    permission_class = [permissions.IsAuthenticated]
    serializer_class = AvailabilitySerializer
    queryset = Availability.objects.none()

    def get_queryset(self):
        return Availability.objects.filter(user=self.request.user, user__user_type=2)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response(_(str(e) + ' CP-101'), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def set_availability(self, request):
        request_user = self.request.user
        if request_user.user_type != 3:
            return Response({"error": _('Only driver can set availability')}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            for availability in request.data:
                Availability.objects.filter(user=request_user, date=availability['date']).delete()
                if availability['whole_day']:
                    data = {
                        "user": request_user,
                        "day": availability['day'],
                        "date": availability['date'],
                        "whole_day": True
                    }
                    Availability.objects.create(**data)
                else:
                    for time in availability['time']:
                        data = {
                            "user": request_user,
                            "day": availability['day'],
                            "date": availability['date'],
                            "whole_day": False,
                            "start_time": time['start_time'],
                            "end_time": time['end_time']
                        }
                        Availability.objects.create(**data)
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": _(str(e)+'[DA-101]')}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get']) # list fromat
    def list_availabilities(self, request):
        today = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        queryset = Availability.objects.filter(user=self.request.user, date__gte=today, is_active=True)
        serializer = AvailabilitySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get']) # json fromat
    def get_availabilities(self, request):
        today = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        queryset = Availability.objects.filter(user=self.request.user, date__gte=today, is_active=True)
        data_list = []
        for distinct_date in queryset.values('date').order_by('date').distinct():
            ids = []
            time_set = []
            for availabilty in queryset.filter(date=distinct_date['date']):
                ids.insert(len(ids), availabilty.id)
                if not availabilty.whole_day:
                    time_set.insert(len(time_set), {
                        "id": availabilty.id,
                        "start_date": availabilty.start_time,
                        "end_date": availabilty.end_time,
                    })

                availability_day = availabilty.day
                availability_date = distinct_date['date']
                whole_day = availabilty.whole_day

            data_list.insert(len(data_list), {
                "availabilty_id": ids,
                "day": availability_day,
                "date": availability_date,
                "whole_day": whole_day,
                "time": time_set
            })
        return Response(data_list)

    @action(detail=False, methods=['delete'])
    def delete_availability_by_id(self, request):
        queryset = get_object_or_404(Availability, pk=request.data["availability_id"])
        queryset.delete()
        return Response({"success": "Data deleted successfully."})

    @action(detail=False, methods=['delete'])
    def delete_availability_by_date(self, request):
        queryset = Availability.objects.filter(user=self.request.user, date=request.data['date'])
        if not queryset.exists():
            return Response({"error": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        queryset.delete()
        return Response({"success": "Data deleted successfully."})

    @action(detail=False, methods=['delete '])
    def delete_availabilities(self, request):
        Availability.objects.filter(user=self.request.user).delete()
        return Response({"success": "Data deleted successfully."})
