from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    DEVICE_TYPES = [
        ('temperature', 'Temperature Sensor'),
        ('humidity', 'Humidity Sensor'),
        ('pressure', 'Pressure Sensor'),
        ('motion', 'Motion Sensor'),
        ('power', 'Power Meter'),
        ('other', 'Other'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=100)
    device_id = models.CharField(max_length=64, unique=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES, default='other')
    location = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.device_id})'


class Reading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='readings')
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.device.name}: {self.value} {self.unit} @ {self.timestamp}'


class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='alerts')
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    threshold = models.FloatField(null=True, blank=True)
    triggered_value = models.FloatField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.severity.upper()}] {self.device.name}: {self.message}'
