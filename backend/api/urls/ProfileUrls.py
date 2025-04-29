"""
Profile Urls.
"""

from django.urls import path
from api.views import ProfileViews

app_name = "Profile"

urlpatterns = [
    path(
        "update/",
        ProfileViews.UpdateProfileView.as_view(),
        name="update-profile",
    ),
    path("status/", ProfileViews.UserStatusView.as_view(), name="user-status"),
]
