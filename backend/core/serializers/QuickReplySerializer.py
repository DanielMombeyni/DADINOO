# ---------------------------------------------------------------------------- #
#                            Quick Reply Serializer                            #
# ---------------------------------------------------------------------------- #
from rest_framework import serializers
from core.models import QuickReply


class QuickReplySerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = QuickReply
        fields = ["id", "text", "role"]

    def get_role(self, obj):
        return obj.get_role_display()
