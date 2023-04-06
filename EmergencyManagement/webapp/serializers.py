from django.contrib.auth.models import User, Group
from .models import Building, EmergencyModePollResult, EmergencyModeIndicator, DeviceCount
from rest_framework import serializers


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('uuid','deviceCount',)

class EmergencyModePollResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyModePollResult
        fields = ("id", "status", "lat", "long", "created_at")

class EmergencyModeIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyModeIndicator
        fields = ("enabled")


class DeviceCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceCount
        fields = ('building','device_count',)