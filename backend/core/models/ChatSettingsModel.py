"""
ChatSettings Model.
"""

from django.db import models
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin


class ChatSettings(CreatedAtMixin, UpdatedAtMixin):
    """تنظیمات پیام ها"""

    predefined_message = models.TextField(null=True, blank=True)
    additional_prompt = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"ChatSettings #{self.id}"
