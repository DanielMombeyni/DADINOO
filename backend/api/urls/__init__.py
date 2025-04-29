"""
API base urls.
"""

from django.urls import include, path
from . import ProfileUrls, OTPUrls, HomeUrls, PaymentUrls, WalletUrls, ChatUrls

urlpatterns = [
    path("otp/", include(OTPUrls)),
    path("home/", include(HomeUrls)),
    path("chats/", include(ChatUrls)),
    path("wallet/", include(WalletUrls)),
    path("profile/", include(ProfileUrls)),
    path("payment/", include(PaymentUrls)),
]
