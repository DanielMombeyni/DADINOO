"""
User Wallet
"""

from django.db import models
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class Wallet(CreatedAtMixin, UpdatedAtMixin):
    balance = models.DecimalField(max_digits=15, decimal_places=3, default=0.00)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="wallet")
