from django.urls import path
from .views import (
    DeviceListCreateView,
    DeviceDetailView,
    ReadingListCreateView,
    AlertListCreateView,
    AlertResolveView,
)

urlpatterns = [
    path('', DeviceListCreateView.as_view(), name='device-list'),
    path('<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('<int:device_pk>/readings/', ReadingListCreateView.as_view(), name='reading-list'),
    path('<int:device_pk>/alerts/', AlertListCreateView.as_view(), name='alert-list'),
    path('<int:device_pk>/alerts/<int:alert_pk>/resolve/', AlertResolveView.as_view(), name='alert-resolve'),
]
