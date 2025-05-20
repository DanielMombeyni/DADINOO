"""
Chat serializer.
"""

from django.contrib.auth import get_user_model, authenticate  # type:ignore

from rest_framework import serializers  # type:ignore

from django.utils.timezone import now  # type:ignore

from core.utils.DynamicModelSerializer import DynamicFieldsModelSerializer

from core.models import Chat, ChatSettings, Message

User = get_user_model()


class ChatSerializer(DynamicFieldsModelSerializer):
    # postman_name = serializers.CharField(source="postman.name", read_only=True)
    # postman_avatar = serializers.CharField(source="postman.avatar", read_only=True)
    plan_id = serializers.CharField(source="plan.id", read_only=True)
    name = serializers.CharField(source="plan.name", read_only=True)
    # avatar = serializers.CharField(source="plan.logo.url", read_only=True)
    last_message = serializers.SerializerMethodField()
    # unread_count = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "id",
            "plan_id",
            # "postman_name",
            # "postman_avatar",
            "name",
            "status",
            "avatar",
            "start_time",
            "end_time",
            "last_message",
            # "unread_count",
            "updated_at",
        ]

    def get_last_message(self, obj):
        return obj.messages.last().message_text if obj.messages.exists() else None

    def get_avatar(self, obj):
        if obj.plan.logo:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.plan.logo.url)

    # def get_unread_count(self, obj):
    #     # منطق شمارش پیام‌های خوانده نشده
    #     return obj.messages.filter(is_read=False).count()


class ChatSettingsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ChatSettings
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "chat", "sender", "sender_type", "message_text", "sent_at"]
