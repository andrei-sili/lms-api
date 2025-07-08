# apps/courses/serializers.py

from rest_framework import serializers
from apps.courses.models import Course, Category, CourseCategory
from apps.users.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'teacher',
            'created_at',
            'price',
        ]
        read_only_fields = ['id', 'teacher', 'created_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
        ]

        read_only_fields = ['id']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Category name cannot be empty.")
        return value


class CourseCategorySerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = CourseCategory
        fields = [
            'id',
            'course',
            'category',
        ]

        read_only_fields = ['id']

    def validate(self, attrs):
        if CourseCategory.objects.filter(course=attrs['course'], category=attrs['category']).exists():
            raise serializers.ValidationError("This course-category relation already exists.")
        return attrs