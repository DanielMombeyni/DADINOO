"""
Chats Model.
"""

from django.db import models
from django.contrib.auth import get_user_model
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin


User = get_user_model()


class Status(models.TextChoices):
    OPEN = "open", "Open"
    CLOSED = "closed", "Closed"


class Chat(CreatedAtMixin, UpdatedAtMixin):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postman = models.ForeignKey(
        "Postman", on_delete=models.CASCADE, related_name="chats"
    )
    # ai_key = models.ForeignKey(
    #     "AIModel", on_delete=models.CASCADE
    # )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.OPEN
    )

    def __str__(self):
        return f"Chat with {self.user.username} - Status: {self.status}"
