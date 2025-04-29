from rest_framework import serializers
from core.models import User, OTP


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        if len(value) != 11 or not value.startswith("09") or not value.isdigit():
            raise serializers.ValidationError(
                "شماره تلفن باید با 09 شروع شود و دقیقاً 11 رقم عددی باشد."
            )
        # if not User.objects.filter(phone_number=value).exists():
        #     raise serializers.ValidationError("کاربری با این شماره وجود ندارد.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

    def create(self, validated_data):
        otp = OTP.objects.create(**validated_data)
        return otp
