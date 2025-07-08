# apps/courses/admin.py
from django.contrib import admin
from .models import Course, Category, CourseCategory

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(CourseCategory)
