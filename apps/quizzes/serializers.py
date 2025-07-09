# apps/quiz/serializers.py

from rest_framework import serializers
from apps.quizzes.models import Quiz, Question, Answer


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            'title',
            'lesson',
            'created_at'
        ]
        read_only_fields = ['id', 'lesson', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'text',
            'quiz'
        ]
        read_only_fields = ['id', 'quiz']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'text',
            'question',
            'is_correct'
        ]
        read_only_fields = ['id']