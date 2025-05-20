"""
Chats Model.
"""

from django.db import models
from django.contrib.auth import get_user_model
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin
from django.core.exceptions import ValidationError


User = get_user_model()


class Status(models.TextChoices):
    OPEN = "open", "Open"
    CLOSED = "closed", "Closed"


class Chat(CreatedAtMixin, UpdatedAtMixin):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # postman = models.ForeignKey(
    #     "Postman", on_delete=models.CASCADE, related_name="chats"
    # )
    plan = models.ForeignKey("Plan", on_delete=models.SET_NULL, null=True)
    # ai_key = models.ForeignKey(
    #     "AIModel", on_delete=models.CASCADE
    # )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.OPEN
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "plan"],
                name="unique_chat_per_user_plan",
            )
        ]

    def __str__(self):
        return f"Chat with {self.user} - Status: {self.status}"

    def clean(self):
        """
        Validate that the user doesn't have another open chat with the same plan.
        """
        if self.pk is None:
            if Chat.objects.filter(user=self.user, plan=self.plan).exists():
                raise ValidationError("User already has a chat with this plan.")

    def save(self, *args, **kwargs):
        """
        Override save to include validation.
        """
        self.clean()
        super().save(*args, **kwargs)
