# apps/lessons/views.py

from rest_framework import viewsets
from apps.courses.permissions import IsOwnerTeacherOrReadOnly
from apps.lessons.models import Lesson
from apps.lessons.serializers import LessonSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerTeacherOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

