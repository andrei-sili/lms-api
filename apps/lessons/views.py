# apps/lessons/views.py

from rest_framework import viewsets
from apps.courses.permissions import IsOwnerTeacherOrReadOnly
from apps.lessons.models import Lesson
from apps.lessons.serializers import LessonReadSerializer, LessonWriteSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerTeacherOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonReadSerializer
        return LessonWriteSerializer

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


