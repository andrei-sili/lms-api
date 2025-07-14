#  apps/lessons/urls.py

from rest_framework.routers import DefaultRouter
from apps.lessons.views import LessonViewSet, AttachmentViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'', LessonViewSet, basename='lessons')
router.register(r'attachments', AttachmentViewSet, basename='attachment')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls
