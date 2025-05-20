"""
User Wallet
"""

from decimal import Decimal
from django.db import models
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class Wallet(CreatedAtMixin, UpdatedAtMixin):
    balance = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name="wallet"
    )

    def spend(self, amount: Decimal, fee_percent: Decimal = Decimal("0.0")):
        """
        کاهش سکه با احتساب درصد کارمزد
        """
        fee = amount * (fee_percent / Decimal("100"))
        total = amount + fee
        if self.balance >= total:
            self.balance -= total
            self.save()
            return True
        return False

    def deposit(self, amount: Decimal):
        """
        افزایش موجودی کیف پول
        """
        self.balance += amount
        self.save()
