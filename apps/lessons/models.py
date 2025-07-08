# apps/lessons/models.py

from django.db import models

from apps.courses.models import Course


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    created_ad = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
