# apps/lessons/serializers.py

from rest_framework import serializers

from apps.courses.serializers import CourseSerializer
from apps.lessons.models import Lesson
from apps.quizzes.serializers import QuizSerializer


class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'title',
            'content',
            'video_url',
            'order',
            'course',
            'quizzes',
            'created_at'
            'created_by'
        ]

        read_only_fields = ['id', 'course', 'created_at', 'created_by']
