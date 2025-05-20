"""
Signals
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from core.models import Wallet
from django.conf import settings

User = get_user_model()


@receiver(post_save, sender=User)
def create_wallet_for_new_user(sender, instance, created, **kwargs):
    """Automatically create a wallet for the new user."""
    if created:
        initial_balance = getattr(settings, "DEFAULT_INITIAL_WALLET_BALANCE", 0.0)
        Wallet.objects.create(user=instance, balance=initial_balance)
