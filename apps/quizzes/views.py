# apps/quizzes/views.py

from rest_framework import viewsets
from apps.courses.permissions import IsOwnerTeacherOrReadOnly
from apps.quizzes.models import Quiz, Question, Answer
from apps.quizzes.serializers import QuizReadSerializer, QuestionSerializer, AnswerSerializer, QuizWriteSerializer


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
