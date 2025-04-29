"""
User serializer.
"""

from django.contrib.auth import get_user_model, authenticate  # type:ignore

from rest_framework import serializers  # type:ignore

from django.utils.timezone import now  # type:ignore

from core.utils.DynamicModelSerializer import DynamicFieldsModelSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            # "password",
        ]
        read_only_fields = [
            "id",
            "phone_number",
        ]

        # extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return a user."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
