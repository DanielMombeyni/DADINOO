"""
Views for the Auth API.
"""

from rest_framework import generics, authentication, permissions  # type:ignore
from rest_framework.authtoken.views import ObtainAuthToken  # type:ignore
from rest_framework.settings import api_settings  # type:ignore
from django.contrib.auth import get_user_model  # type:ignore
from rest_framework.response import Response  # type:ignore
from rest_framework import status  # type:ignore
from core.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve & return the authenticated user."""

        return self.request.user


class PasswordResetRequestView(generics.CreateAPIView):
    """
    View to request a password reset.
    Accepts an email, validates it, and sends a reset token to the user.
    """

    serializer_class = PasswordResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This triggers token generation and email sending
            return Response(
                {"detail": "Password reset instructions have been sent to your email."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(generics.RetrieveUpdateAPIView):
    """View to confirm and reset the password."""

    serializer_class = PasswordResetConfirmSerializer

    def get_object(self):
        """Retrieve the user object by token."""
        token = self.request.data.get("token")
        if not token:
            self._invalid_token_response()

        user = get_user_model().objects.filter(password_reset_token=token).first()
        if not user:
            self._invalid_token_response()
        return user

    def _invalid_token_response(self):
        """Helper method for handling invalid/expired tokens."""
        response = Response(
            {"detail": "Invalid or expired token."},
            status=status.HTTP_400_BAD_REQUEST,
        )
        response.exception = True
        raise response.exception

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Password has been reset successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
