# apps/lessons/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from apps.courses.permissions import IsOwnerTeacherOrReadOnly, HasActiveSubscription
from apps.lessons.models import Lesson, Attachment, Comment, LessonProgress
from apps.lessons.permissions import IsEnrolledInLessonCourse, IsCommentOwner, IsOwnerOfProgress
from apps.lessons.serializers import LessonReadSerializer, LessonWriteSerializer, AttachmentSerializer, \
    CommentSerializer, LessonProgressSerializer


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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscription, IsEnrolledInLessonCourse, IsCommentOwner]

    def get_queryset(self):
        return Comment.objects.select_related('user', 'lesson')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscription, IsEnrolledInLessonCourse, IsOwnerOfProgress]

    def get_queryset(self):
        return LessonProgress.objects.filter(user=self.request.user).select_related('lesson')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, completed_at=timezone.now())