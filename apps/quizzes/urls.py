#  apps/quizzes/urls.py

from rest_framework.routers import DefaultRouter

from apps.quizzes.views import QuizViewSet, QuestionViewSet, AnswerViewSet, UserQuizAttemptViewSet

router = DefaultRouter()
router.register(r'', QuizViewSet, basename='quizzes')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')
router.register(r'attempts', UserQuizAttemptViewSet, basename='attempts')

urlpatterns = router.urls
