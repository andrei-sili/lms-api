# apps/quizzes/models.py
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.lessons.models import Lesson
from apps.users.models import User


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


class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempted_quizzes')
    score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.quiz} ({self.score})"
