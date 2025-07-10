#  apps/quizzes/urls.py

from rest_framework.routers import DefaultRouter

from apps.quizzes.views import QuizViewSet, QuestionViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r'', QuizViewSet, basename='quizzes')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')

urlpatterns = router.urls
