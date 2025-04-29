"""
User Discount Code.
"""

from django.db import models
from core.models.BaseModels import CreatedAtMixin
from django.contrib.auth import get_user_model
from core.models.DiscountCodeModel import DiscountCode

User = get_user_model()


class UserDiscountCode(CreatedAtMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discount")
    discount_code = models.ForeignKey(
        DiscountCode, on_delete=models.CASCADE, related_name="discount"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "discount_code"], name="user_discount_unique"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.discount_code.code}"
