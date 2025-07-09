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

    def validate(self, attrs):
        title = attrs.get('title')
        lesson = self.instance.lesson if self.instance else attrs.get('lesson')
        if Quiz.objects.filter(title=title, lesson=lesson).exists():
            raise serializers.ValidationError("This lesson already has a quiz with this title.")
        return attrs


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'text',
            'question',
            'is_correct'
        ]
        read_only_fields = ['id']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Answer text cannot be empty.")
        return value


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Question
        fields = [
                'text',
                'quiz',
                'answers'
        ]

    def validate(self, attrs):
        answers_data = attrs.get('answers', [])
        if answers_data:
            if len(answers_data) < 2:
                raise serializers.ValidationError("A question must have at least 2 answers.")
            if sum(1 for a in answers_data if a.get('is_correct')) != 1:
                raise serializers.ValidationError("There must be exactly one correct answer.")
        return attrs
