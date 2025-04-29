"""
Attendance Guide Settings Model
"""

from django.db import models
from core.models.BaseModels import CreatedAtMixin, UpdatedAtMixin


class AttendanceGuideSettings(CreatedAtMixin, UpdatedAtMixin):
    """تنظیمات راهنمای حضور"""

    predefined_message = models.TextField(null=True, blank=True)
    questions = models.TextField(null=True, blank=True)
    prompt = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"AttendanceGuideSettings #{self.id}"
