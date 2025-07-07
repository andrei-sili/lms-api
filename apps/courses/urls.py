#  apps/courses/urls.py

from rest_framework.routers import DefaultRouter
from apps.courses.views import CourseViewSet, CourseCategoryViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'course_categories', CourseCategoryViewSet, basename='course_category')

urlpatterns = router.urls
