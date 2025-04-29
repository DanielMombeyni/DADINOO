"""
Chat Views.
"""

from rest_framework import generics, permissions
from core.models import Chat
from core.serializers import ChatSerializer


class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user).order_by("-start_time")
