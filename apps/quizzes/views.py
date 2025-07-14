# apps/quizzes/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.courses.permissions import IsOwnerTeacherOrReadOnly, HasActiveSubscription
from apps.quizzes.models import Quiz, Question, Answer, UserQuizAttempt
from apps.quizzes.serializers import QuizReadSerializer, QuestionSerializer, AnswerSerializer, QuizWriteSerializer, \
    UserQuizAttemptSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    permission_classes = [IsOwnerTeacherOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return QuizReadSerializer
        return QuizWriteSerializer

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerTeacherOrReadOnly]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerTeacherOrReadOnly]


class UserQuizAttemptViewSet(viewsets.ModelViewSet):
    serializer_class = UserQuizAttemptSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscription]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserQuizAttempt.objects.all()
        return UserQuizAttempt.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
