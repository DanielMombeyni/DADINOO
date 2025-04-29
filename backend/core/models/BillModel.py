"""
Bills Model.
"""

from django.db import models
from django.contrib.auth import get_user_model
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin

User = get_user_model()


class Bill(CreatedAtMixin, UpdatedAtMixin):
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE, related_name="bills")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bills")
    postman = models.ForeignKey(
        "Postman", on_delete=models.CASCADE, related_name="postman_bills"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"Bill: {self.title} - {self.chat.id}"
