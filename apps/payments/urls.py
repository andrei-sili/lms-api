# apps/payments/urls.py

from rest_framework.routers import DefaultRouter
from apps.payments.views import PaymentViewSet

router = DefaultRouter()
router.register(r'', PaymentViewSet, basename='payments')

urlpatterns = router.urls
