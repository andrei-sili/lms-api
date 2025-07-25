# apps/users/urls.py

from rest_framework.routers import DefaultRouter

from apps.users.views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = router.urls
