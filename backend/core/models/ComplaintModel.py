"""
Complaint Model.
"""

from django.db import models
from django.contrib.auth import get_user_model
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin

User = get_user_model()


class ResponseEvaluation(models.TextChoices):
    APPROVE = "approve", "Approve"
    REJECT = "reject", "Reject"
    PENDING = "pending", "Pending"


class Complaint(CreatedAtMixin, UpdatedAtMixin):
    """اعتراضات کاربران"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complaints")
    chat = models.ForeignKey(
        "Chat", on_delete=models.CASCADE, related_name="complaints"
    )
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, related_name="complaints"
    )
    complaint_text = models.TextField()
    response_evaluation = models.CharField(
        max_length=10,
        choices=ResponseEvaluation.choices,
        default=ResponseEvaluation.PENDING,
    )
    admin_response = models.TextField(null=True, blank=True)
    resolution_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Complaint by {self.user.username} - Status: {self.response_evaluation}"
