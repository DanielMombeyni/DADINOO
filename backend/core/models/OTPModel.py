"""
OTP Model.
"""

from django.db import models
from core.models.BaseModels import CreatedAtMixin
from django.utils import timezone

class OTP(CreatedAtMixin):
    phone_number = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=2)

    def __str__(self):
        return f"{self.phone_number} - {self.code}"
