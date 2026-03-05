from rest_framework import serializers
from .models import Device, Reading, Alert


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ('id', 'value', 'unit', 'timestamp')
        read_only_fields = ('id', 'timestamp')


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = (
            'id', 'device', 'message', 'severity',
            'threshold', 'triggered_value',
            'is_resolved', 'created_at', 'resolved_at',
        )
        read_only_fields = ('id', 'created_at')


class DeviceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    latest_reading = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = (
            'id', 'owner', 'name', 'device_id', 'device_type',
            'location', 'is_active', 'latest_reading',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

    def get_latest_reading(self, obj):
        reading = obj.readings.first()
        if reading:
            return ReadingSerializer(reading).data
        return None


class DeviceListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Device
        fields = ('id', 'name', 'device_id', 'device_type', 'location', 'is_active', 'owner')
