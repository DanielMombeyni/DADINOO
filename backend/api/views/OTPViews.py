"""
OTP Views
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.utils import timezone
from core.models import User, OTP
from core.serializers import SendOTPSerializer, VerifyOTPSerializer
from django.contrib.auth import login
from core.utils.GenratorToken import generate_token
from rest_framework.authtoken.models import Token
from core.services.otp_service import OTPService
import asyncio
import random


class SendOTPView(generics.GenericAPIView):
    serializer_class = SendOTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]

        # حذف OTPهای قدیمی
        OTP.objects.filter(phone_number=phone_number).delete()

        code = str(random.randint(100000, 999999))
        OTP.objects.create(phone_number=phone_number, code=code)

        # چک کنیم کاربر وجود داره یا نه
        user_exists = User.objects.filter(phone_number=phone_number).exists()

        otp_service = OTPService()

        try:
            asyncio.run(otp_service.send_pattern_otp(phone_number, code))
        except Exception as e:
            return Response(
                {"detail": "خطا در ارسال پیامک", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"detail": "OTP ارسال شد", "user_exists": user_exists},
            status=status.HTTP_200_OK,
        )


class VerifyOTPView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        code = serializer.validated_data["code"]

        try:
            otp = OTP.objects.get(
                phone_number=phone_number, code=code, is_verified=False
            )
        except OTP.DoesNotExist:
            return Response(
                {"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

        if otp.is_expired():
            otp.delete()
            return Response(
                {"detail": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST
            )

        otp.is_verified = True
        otp.save()

        user, created = User.objects.get_or_create(phone_number=phone_number)

        # Use DRF's Token model for consistency with CreateTokenView
        token, created = Token.objects.get_or_create(user=user)

        # Check if we should delete the old token for security
        if not created:
            token.delete()
            token = Token.objects.create(user=user)

        # Check profile completeness
        profile_incomplete = not (user.first_name and user.last_name)

        return Response(
            {
                "detail": "Login successful",
                "token": {
                    "access_token": token.key,
                    "refresh_token": "",  # Add if using refresh tokens
                },
                "new_user": created,
                "profile_incomplete": profile_incomplete,
            },
            status=status.HTTP_200_OK,
        )
