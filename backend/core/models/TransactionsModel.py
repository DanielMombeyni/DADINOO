"""
Wallet Transactions.
"""

from django.db import models
from core.models.BaseModels import CreatedAtMixin
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class TransactionType(models.IntegerChoices):
    Deposit = 1, "Deposit"
    Withdrawal = 2, "Withdrawal"
    REFUND = 3, "Refund"
    Charge = 4, "Charge"
    Discount = 5, "Discount"


class TransactionStatus(models.IntegerChoices):
    Pending = 1, "Pending"
    Success = 2, "Success"
    Failed = 3, "Failed"


class Transaction(CreatedAtMixin):
    amount = models.DecimalField(max_digits=15, decimal_places=3, default=0.00)
    transaction_type = models.IntegerField(
        choices=TransactionType.choices, default=TransactionType.Deposit
    )
    status = models.IntegerField(
        choices=TransactionStatus.choices, default=TransactionStatus.Success
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="transaction"
    )
    source_account = models.CharField(max_length=255, null=True, blank=True)
    destination_account = models.CharField(max_length=255, null=True, blank=True)
    related_id = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    transaction_date = models.DateTimeField(default=timezone.now)
