from django.contrib.auth.models import User
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema

from .serializers import RegisterSerializer, UserSerializer


@extend_schema(tags=['Auth'])
class RegisterView(generics.CreateAPIView):
    """Register a new user account."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=['Auth'])
class MeView(generics.RetrieveAPIView):
    """Get current authenticated user info."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
