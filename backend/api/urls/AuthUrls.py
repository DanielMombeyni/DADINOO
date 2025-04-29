"""
Auth Urls.
"""

from django.urls import path
from api.views import AuthViews

app_name = "Auth"

urlpatterns = [
    path("create/", AuthViews.CreateUserView.as_view(), name="create"),
    path("token/", AuthViews.CreateTokenView.as_view(), name="token"),
    path("profile/", AuthViews.ManageUserView.as_view(), name="profile"),
    path(
        "password-reset-request/",
        AuthViews.PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password-reset-confirm/",
        AuthViews.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]
