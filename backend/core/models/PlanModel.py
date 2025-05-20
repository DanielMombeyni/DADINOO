"""
Plans models.
"""

from django.db import models
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin


class Plan(CreatedAtMixin, UpdatedAtMixin):
    """"""

    logo = models.ImageField(upload_to="plans/logos/", null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f" ID: {self.id} Plan name: {self.name}"
