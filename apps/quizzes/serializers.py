# apps/quiz/serializers.py

from rest_framework import serializers
from apps.quizzes.models import Quiz, Question, Answer


class QuizReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'lesson',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        title = attrs.get('title')
        lesson = self.instance.lesson if self.instance else attrs.get('lesson')
        if Quiz.objects.filter(title=title, lesson=lesson).exists():
            raise serializers.ValidationError("This lesson already has a quiz with this title.")
        return attrs


class QuizWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['title', 'lesson']

    def validate(self, attrs):
        title = attrs.get('title')
        lesson = attrs.get('lesson')
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
    answers_list = AnswerSerializer(source='answers', many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
                'text',
                'quiz',
                'answers',
                'answers_list',
        ]

    def validate(self, attrs):
        answers_data = attrs.get('answers', [])
        if answers_data:
            if len(answers_data) < 2:
                raise serializers.ValidationError("A question must have at least 2 answers.")
            if sum(1 for a in answers_data if a.get('is_correct')) != 1:
                raise serializers.ValidationError("There must be exactly one correct answer.")
        return attrs

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)

        return question

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers', None)
        instance.text = validated_data.get('text', instance.text)
        instance.quiz = validated_data.get('quiz', instance.quiz)
        instance.save()

        if answers_data is not None:
            instance.answers.all().delete()
            for answer_data in answers_data:
                Answer.objects.create(question=instance, **answer_data)

        return instance
