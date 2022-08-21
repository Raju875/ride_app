from datetime import timedelta, datetime, date
import calendar
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from schedule_ride.models import *


class ScheduleRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleRide
        fields = '__all__'

        extra_kwargs = {
            'customer': {
                'read_only': True
            },
            'end_at': {
                'read_only': True
            },
            'total_price': {
                'read_only': True
            },
            'is_canceled': {
                'read_only': True
            },
            'canceled_by': {
                'read_only': True
            },
            'is_active': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            },
            'updated_at': {
                'read_only': True
            },
        }

    def validate(self, attrs):  
        request_user = self.context['request'].user
        if request_user.user_type != 2:
            raise serializers.ValidationError({
                "error": _("Only customr are allowed to create schedule request")})

        total_hours = attrs['total_hours']
        # hour_separator = ':'
        if not ':' in total_hours:
            raise serializers.ValidationError({'total_hours': _('Invalid time format!')})
        input_hours = total_hours.split(':', 2)
        hours = int(input_hours[0])
        minutes = int(input_hours[1])
        if hours>23 or minutes>59:
            raise serializers.ValidationError({'total_hours': _('Invalid time input!')})
        
        my_datetime = datetime.combine(attrs['date'], datetime.min.time()) # 2022-07-28 00:00:00
        start_time = datetime.strptime(str(attrs['start_time']), '%H:%M:%S').time() # 14:17:00
        start_at = datetime.combine(my_datetime, start_time)
        end_at = start_at + timedelta(hours=hours, minutes=minutes) # 2022-07-28 15:28:00

        if ScheduleRide.objects.filter(driver=attrs['driver'], date=attrs['date'], end_at__gte=start_at, is_canceled=False, is_active=True).exists():
            raise serializers.ValidationError({
                'error': _("The driver is already booked in this schedule time.")
            })
        
        price_per_hour = 50
        attrs['total_price'] = round((price_per_hour * (hours + (minutes/60))), 3)
        attrs['end_at'] = end_at
        attrs['day'] = calendar.day_name[my_datetime.weekday()]
        return attrs

    def create(self, validated_data):
        return ScheduleRide.objects.create(**validated_data)


class CancelScheduleRideSerializer(serializers.ModelSerializer):
    is_canceled = serializers.BooleanField()
    
    class Meta:
        model = ScheduleRide
        fields = ['is_canceled']

    def update(self, instance, validated_data):
        try:
            request_user = self.context['request'].user
            instance.is_canceled = True
            instance.canceled_by = request_user.user_type
            instance.is_active = False
            instance.save()
            
            return instance
        except Exception as e:
            raise serializers.ValidationError({'error': _(str(e) + '[SR-101]')})
