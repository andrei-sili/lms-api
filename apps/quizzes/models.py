# apps/quizzes/models.py

from django.db import models
from apps.lessons.models import Lesson


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"Question: {self.text[:50]}..."


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField(blank=False, null=False)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer: {self.text[:50]}..."