# apps/quizzes/views.py

from rest_framework import viewsets
from apps.courses.permissions import IsOwnerTeacherOrReadOnly
from apps.quizzes.models import Quiz, Question, Answer
from apps.quizzes.serializers import QuizSerializer, QuestionSerializer, AnswerSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsOwnerTeacherOrReadOnly]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerTeacherOrReadOnly]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerTeacherOrReadOnly]
