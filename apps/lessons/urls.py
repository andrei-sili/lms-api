#  apps/lessons/urls.py

from rest_framework.routers import DefaultRouter
from apps.lessons.views import LessonViewSet

router = DefaultRouter()
router.register(r'', LessonViewSet, basename='lessons')

urlpatterns = router.urls