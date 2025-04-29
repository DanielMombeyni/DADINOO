"""
OTP Urls.
"""

from django.urls import path
from api.views import OTPViews

app_name = "OTP"

urlpatterns = [
    path("send-otp/", OTPViews.SendOTPView.as_view()),
    path("verify-otp/", OTPViews.VerifyOTPView.as_view()),
]
