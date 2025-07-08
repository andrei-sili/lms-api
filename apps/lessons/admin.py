# apps/lessons/admin.py

from django.contrib import admin
from apps.lessons.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course',)
    search_fields = ('title', 'content')
    ordering = ('course', 'order')
