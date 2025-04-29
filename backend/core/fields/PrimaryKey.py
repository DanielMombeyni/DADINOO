"""
Custom Field PK
"""

import string
import random
from django.db import models
import uuid


class PrimaryKeyField(models.CharField):
    description = "A custom primary key field generating unique IDs with a prefix and random suffix."

    def __init__(self, prefix: str, length: int = 6, *args, **kwargs):
        self.prefix = prefix
        self.length = length
        kwargs["max_length"] = len(self.prefix) + self.length
        kwargs["unique"] = True
        kwargs["primary_key"] = True
        kwargs["auto_created"] = True
        super().__init__(*args, **kwargs)

    def generate_unique_id(self):
        return f"{self.prefix}{str(uuid.uuid4().int)[:self.length]}"

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if not value:
            value = self.generate_unique_id()
            setattr(model_instance, self.attname, value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["prefix"] = self.prefix
        kwargs["length"] = self.length
        return name, path, args, kwargs
