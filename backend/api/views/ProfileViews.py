"""
Profile Views.
"""

from rest_framework import generics, permissions, views, response
from core.serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.utils.timezone import now


User = get_user_model()


class UpdateProfileView(generics.UpdateAPIView):
    """Update User Profile info."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserStatusView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        print("Headers:", request.headers)
        print("Authorization header:", request.headers.get("Authorization"))
        print("User:", request.user)
        user = request.user
        token_expired = False
        profile_completed = False

        if user.password_reset_token_expires:
            token_expired = now() > user.password_reset_token_expires

        if user.first_name and user.last_name:
            profile_completed = True

        return response.Response(
            {
                "token_expired": token_expired,
                "profile_completed": profile_completed,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone_number,
            }
        )
