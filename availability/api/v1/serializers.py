from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from availability.models import *


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        exclude = ['is_active', 'created_at', 'updated_at']

        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'driver': {
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
            }
        }