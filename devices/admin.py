from django.contrib import admin
from .models import Device, Reading, Alert

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_id', 'device_type', 'location', 'is_active', 'owner')
    list_filter = ('device_type', 'is_active')
    search_fields = ('name', 'device_id')

@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ('device', 'value', 'unit', 'timestamp')
    list_filter = ('device',)

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('device', 'severity', 'message', 'is_resolved', 'created_at')
    list_filter = ('severity', 'is_resolved')
