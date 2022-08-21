import datetime
from rest_framework import serializers
from tracking import models



class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tracking
        exclude = ('driver','customer')

    def update(self, instance, validated_data):
        instance.updated_at = datetime.datetime.now()
        return super().update(instance, validated_data)

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Request
        exclude = ('driver','is_accepted','customer')

    def create(self, validated_data):
        user = self.context['request'].user
        if user.user_type == 3:
            raise serializers.ValidationError("Drivers are not allowed to create request")
        return models.Request.objects.create(
            **validated_data
        )
