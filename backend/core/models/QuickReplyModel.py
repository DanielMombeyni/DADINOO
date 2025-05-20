# ---------------------------------------------------------------------------- #
#                             Quick Reply Question                             #
# ---------------------------------------------------------------------------- #
from django.db import models


class QuickReply(models.Model):
    ROLE_CHOICES = [
        ("user", "کاربر"),
        ("lawyer", "وکیل"),
        ("general", "عمومی"),
    ]

    text = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="general")
    is_active = models.BooleanField(default=True)
    plan = models.ForeignKey(
        "Plan", on_delete=models.CASCADE, related_name="quick_replies"
    )

    def __str__(self):
        return f"{self.text} ({self.get_role_display()})"
