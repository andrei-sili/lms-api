#  apps/courses/views.py

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Course, Category, CourseCategory, Enrollment
from .serializers import CourseSerializer, CategorySerializer, CourseCategorySerializer, EnrollmentSerializer
from .permissions import IsOwnerTeacherOrReadOnly, IsAdminOrReadOnly, HasActiveSubscription


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & IsOwnerTeacherOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = [IsAuthenticated & IsOwnerTeacherOrReadOnly]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if self.request.user != course.teacher or self.request.user.role != 'teacher':
            raise PermissionDenied("You don't have permission to associate categories to this course.")
        serializer.save()


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('user', 'course').all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated & HasActiveSubscription]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
