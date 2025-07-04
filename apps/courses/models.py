# apps/courses/models.py

from django.db import models
from apps.users.models import User


class Courses(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateField(auto_now_add=True, editable=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    def __str__(self):
        return self.title


class Categories(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CourseCategories(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.course.title} - {self.category.name}"