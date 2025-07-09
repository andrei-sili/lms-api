# apps/lessons/serializers.py

from rest_framework import serializers
from apps.courses.models import Course
from apps.courses.serializers import CourseSerializer
from apps.lessons.models import Lesson
from apps.quizzes.serializers import QuizReadSerializer


class LessonReadSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    quizzes = QuizReadSerializer(many=True, read_only=True)
    teacher = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'content',
            'video_url',
            'order',
            'course',
            'quizzes',
            'teacher',
            'created_at',
        ]

        read_only_fields = ['id', 'course', 'teacher', 'created_at']


class LessonWriteSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = [
            'title',
            'content',
            'video_url',
            'order',
            'course',
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate(self, attrs):
        course = attrs.get('course')
        teacher = self.context['request'].user
        if course and teacher != course.teacher:
            raise serializers.ValidationError("Only the course teacher can create lessons for this course.")
        return attrs
