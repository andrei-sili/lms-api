# apps/lessons/models.py

from django.db import models
from apps.courses.models import Course
from django.conf import settings


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
