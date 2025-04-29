"""
Discount Code Model.
"""

from django.db import models
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin


class DiscountType(models.TextChoices):
    NEW_USERS = "new_users", "New Users"
    ALL_USERS = "all_users", "All Users"
    SPECIFIC_USERS = "specific_users", "Specific Users"


class DiscountCode(CreatedAtMixin, UpdatedAtMixin):

    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=DiscountType.choices)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code
