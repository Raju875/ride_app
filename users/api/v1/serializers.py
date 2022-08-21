from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from users.models import *


import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        exclude = ['is_active', 'created_at', 'updated_at']

        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'is_approved': {
                'read_only': True
            },
            'is_verify_mail_sent': {
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

    def validate(self, attrs):
        if self.context['request'].user.user_type != 2:
            raise serializers.ValidationError({'error': _('You are not customer!')})
        return attrs


class CustomerDocumentsSerializer(serializers.ModelSerializer):
    document_front_photo = Base64ImageField(max_length=None, required=False)
    document_back_photo = Base64ImageField(max_length=None, required=False)
    face_photo = Base64ImageField(max_length=None, required=False)
    profile_image = Base64ImageField(max_length=None, required=False)

    class Meta:
        model = CustomerDocuments
        exclude = ['user', 'customer', 'is_active', 'created_at', 'updated_at']

        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'customer': {
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

    def validate(self, attrs):
        if self.context['request'].user.user_type != 2:
            raise serializers.ValidationError({'error': _('You are not customer!')})
        return attrs


class DriverProfileSerializer(serializers.ModelSerializer):
    # set_availability = serializers.JSONField(required=False)
    # availability = AvailabilitySerializer(many=True, required=False)
    # vehicle_info = VehicleInfoSerializer(many=False, required=False)

    class Meta:
        model = DriverProfile
        exclude = ['is_active', 'is_verify_mail_sent', 'created_at', 'updated_at']

        extra_kwargs = {
            'user': {
                'read_only': True
            },
            # 'availability': {
            #     'read_only': True
            # },
            'is_approved': {
                'read_only': True
            },
            'is_verify_mail_sent': {
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


    def validate(self, attrs):
        user = self.context['request'].user
        if user.user_type != 3:
            raise serializers.ValidationError({'error': _('This user is not a driver')})
        return attrs


class VehicleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleInfo
        exclude = ['driver', 'user', 'is_active', 'created_at', 'updated_at']

        extra_kwargs = {
            'driver': {
                'read_only': True
            },
            'user': {
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

    def validate(self, data):
        try:
            user = self.context['request'].user
            driver = self.context['request'].user.driver_profile
        except Exception as e:
            raise serializers.ValidationError({'error': _(str(e) + '[VI-101]')})
        from django.db.models import Q
        if self.context['request'].method == 'POST' and VehicleInfo.objects.filter(Q(user=user) | Q(driver=driver)).exists():
            raise serializers.ValidationError({'error': _('You have already submitted vehicle info.')})
        return data
        

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class VerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.IntegerField(required=True, max_value=9999, min_value=1000)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.IntegerField(required=True, max_value=9999, min_value=1000)
    password = serializers.CharField(write_only=True, style={"input_type": 'password'})
    confirm_password = serializers.CharField(write_only=True, style={"input_type": 'password'})
