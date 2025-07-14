#  apps/lessons/urls.py

from rest_framework.routers import DefaultRouter
from apps.lessons.views import LessonViewSet, AttachmentViewSet

router = DefaultRouter()
router.register(r'', LessonViewSet, basename='lessons')
router.register(r'attachments', AttachmentViewSet, basename='attachment')

urlpatterns = router.urls
