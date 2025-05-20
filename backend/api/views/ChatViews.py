"""
Chat Views.
"""

from rest_framework import generics, permissions, response, status
from core.models import Chat, QuickReply
from core.serializers import ChatSerializer, QuickReplySerializer


class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user).order_by("-start_time")


class PlanQuickRepliesView(generics.ListAPIView):
    serializer_class = QuickReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        plan_id = self.kwargs.get("plan_id")
        return QuickReply.objects.filter(plan_id=plan_id, is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return response.Response(
                {"detail": "پلن یافت نشد یا پاسخی موجود نیست."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
