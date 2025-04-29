"""
Complaint Model.
"""

from django.db import models
from django.contrib.auth import get_user_model
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin

User = get_user_model()


class Cost(CreatedAtMixin, UpdatedAtMixin):
    """هزینه ها"""

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    source_account = models.CharField(max_length=255)
    cost_date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return f"{self.source_account} - {self.amount} at {self.cost_date.strftime('%Y-%m-%d')}"
