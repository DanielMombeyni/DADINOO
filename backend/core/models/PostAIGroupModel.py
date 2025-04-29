"""
PostAIGroup Model.
"""

from django.db import models
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin


class PostAIGroup(CreatedAtMixin, UpdatedAtMixin):
    postman = models.ForeignKey(
        "Postman", on_delete=models.CASCADE, related_name="ai_groups"
    )
    ai_group = models.ForeignKey(
        "AIGroup", on_delete=models.CASCADE, related_name="postmen"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["postman", "ai_group"], name="postman_group_unique"
            )
        ]

    def __str__(self):
        return f"{self.postman.name} - {self.ai_group.title}"
