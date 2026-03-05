from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.utils import timezone

from .models import Device, Reading, Alert
from .serializers import DeviceSerializer, DeviceListSerializer, ReadingSerializer, AlertSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, 'owner', None) or getattr(obj, 'device', None).owner
        return owner == request.user


@extend_schema(tags=['Devices'])
@extend_schema_view(
    get=extend_schema(summary='List all devices for the authenticated user'),
    post=extend_schema(summary='Register a new device'),
)
class DeviceListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeviceListSerializer
        return DeviceSerializer

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@extend_schema(tags=['Devices'])
@extend_schema_view(
    get=extend_schema(summary='Retrieve a device'),
    put=extend_schema(summary='Update a device'),
    patch=extend_schema(summary='Partially update a device'),
    delete=extend_schema(summary='Delete a device'),
)
class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)


@extend_schema(tags=['Readings'])
@extend_schema_view(
    get=extend_schema(summary='List readings for a device'),
    post=extend_schema(summary='Submit a new sensor reading'),
)
class ReadingListCreateView(generics.ListCreateAPIView):
    serializer_class = ReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        device = generics.get_object_or_404(
            Device, pk=self.kwargs['device_pk'], owner=self.request.user
        )
        return Reading.objects.filter(device=device)

    def perform_create(self, serializer):
        device = generics.get_object_or_404(
            Device, pk=self.kwargs['device_pk'], owner=self.request.user
        )
        serializer.save(device=device)


@extend_schema(tags=['Alerts'])
@extend_schema_view(
    get=extend_schema(summary='List alerts for a device'),
    post=extend_schema(summary='Create a new alert for a device'),
)
class AlertListCreateView(generics.ListCreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        device = generics.get_object_or_404(
            Device, pk=self.kwargs['device_pk'], owner=self.request.user
        )
        return Alert.objects.filter(device=device)

    def perform_create(self, serializer):
        device = generics.get_object_or_404(
            Device, pk=self.kwargs['device_pk'], owner=self.request.user
        )
        serializer.save(device=device)


@extend_schema(tags=['Alerts'], summary='Resolve an alert')
class AlertResolveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, device_pk, alert_pk):
        device = generics.get_object_or_404(Device, pk=device_pk, owner=request.user)
        alert = generics.get_object_or_404(Alert, pk=alert_pk, device=device)
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.save()
        return Response(AlertSerializer(alert).data)
