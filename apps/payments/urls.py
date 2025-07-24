# apps/payments/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.payments.views import PaymentViewSet, stripe_webhook

router = DefaultRouter()
router.register(r'', PaymentViewSet, basename='payments')
urlpatterns = router.urls + [
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
]
