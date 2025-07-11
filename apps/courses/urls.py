#  apps/courses/urls.py

from rest_framework.routers import DefaultRouter
from apps.courses.views import CourseViewSet, CourseCategoryViewSet, CategoryViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='courses')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'course_categories', CourseCategoryViewSet, basename='course_categories')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
urlpatterns = router.urls
