"""
Declaration Model.
"""

from django.db import models
from django.contrib.auth import get_user_model
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin

User = get_user_model()


class Declaration(CreatedAtMixin, UpdatedAtMixin):
    chat = models.ForeignKey(
        "Chat", on_delete=models.CASCADE, related_name="declarations"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_declarations"
    )
    postman = models.ForeignKey(
        "Postman", on_delete=models.CASCADE, related_name="postman_declarations"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"Declaration: {self.title} - Chat #{self.chat.id}"
