# apps/lessons/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.courses.permissions import IsOwnerTeacherOrReadOnly, HasActiveSubscription
from apps.lessons.models import Lesson, Attachment
from apps.lessons.permissions import IsEnrolledInLessonCourse
from apps.lessons.serializers import LessonReadSerializer, LessonWriteSerializer, AttachmentSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerTeacherOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonReadSerializer
        return LessonWriteSerializer

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscription, IsEnrolledInLessonCourse]