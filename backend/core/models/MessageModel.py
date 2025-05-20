"""
Messages Model.
"""

from django.db import models
from django.contrib.auth import get_user_model
from core.models.BaseModels import CreatedAtMixin

User = get_user_model()


class SenderType(models.TextChoices):
    USER = "user", "User"
    POSTMAN = "postman", "Postman"


class Message(CreatedAtMixin):

    chat = models.ForeignKey("Chat", on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=10, choices=SenderType.choices)
    message_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_type.capitalize()} ({self.sender}) - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
