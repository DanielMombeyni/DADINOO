"""
AIGroup Model.
"""

from django.db import models
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin


class AIGroup(CreatedAtMixin, UpdatedAtMixin):
    """گروه های هوش مصنوعی"""

    title = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to="ai_groups/avatars/", null=True, blank=True)

    def __str__(self):
        return self.title
