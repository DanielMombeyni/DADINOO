"""
User serializer.
"""

from django.contrib.auth import get_user_model, authenticate  # type:ignore

from rest_framework import serializers  # type:ignore

from django.utils.timezone import now  # type:ignore

from core.utils.DynamicModelSerializer import DynamicFieldsModelSerializer

User = get_user_model()


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = "Unable to authenticate with provided credentials."
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for requesting a password reset."""

    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "No user found with this email address."}
            )
        return value

    def save(self):
        """Generate a password reset token and email the user."""
        reset_token = self.user.generate_password_reset_token()
        # send_password_reset_email(self.user, reset_token)
        return self.user


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming and resetting the password."""

    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate_token(self, value):
        try:
            self.user = User.objects.get(password_reset_token=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired token.")

        if self.user.password_reset_token_expires < now():
            raise serializers.ValidationError("Token has expired.")
        return value

    def save(self):
        """Reset the password and clear the token."""
        new_password = self.validated_data["new_password"]
        self.user.set_password(new_password)
        self.user.clear_password_reset_token()
        self.user.save()
        return self.user
