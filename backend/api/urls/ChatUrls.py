"""
Chat Urls.
"""

from django.urls import path
from api.views import ChatViews

app_name = "Chat"

urlpatterns = [
    path("", ChatViews.ChatListView.as_view(), name="chat-list"),
    path(
        "<int:plan_id>/quick-replies/",
        ChatViews.PlanQuickRepliesView.as_view(),
        name="plan-quick-replies",
    ),
]
