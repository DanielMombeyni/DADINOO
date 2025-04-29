"""
BillSettings Model.
"""

from django.db import models
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin


class BillSettings(CreatedAtMixin, UpdatedAtMixin):
    """تنظیمات لوایح"""

    predefined_message = models.TextField(null=True, blank=True)
    questions = models.TextField(null=True, blank=True)
    prompt = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"BillSettings #{self.id}"
