# apps/subscriptions/urls.py

from rest_framework.routers import DefaultRouter

from apps.subscriptions.views import SubscriptionViewSet

router = DefaultRouter()
router.register(r'', SubscriptionViewSet, basename='subscriptions')

urlpatterns = router.urls
