"""
Postman Model.
"""

from django.db import models
from django.contrib.auth import get_user_model
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin

User = get_user_model()


class Postman(CreatedAtMixin, UpdatedAtMixin):
    """ پستچی ها - هوش مصنوعی """
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to="postmen/avatars/", null=True, blank=True)

    def __str__(self):
        return self.name
