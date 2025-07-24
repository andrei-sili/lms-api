# apps/payments/views.py

from rest_framework import viewsets, permissions
from apps.payments.serializers import PaymentSerializer
import stripe
import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

from apps.payments.models import Payment
import logging
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=webhook_secret
        )
        event_id = event['id']
        if Payment.objects.filter(event_id=event_id).exists():
            logger.warning(f"Duplicate event {event_id} ignored.")
            return HttpResponse(status=200)

    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        transaction_id = intent.get('id')

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            payment.status = 'completed'
            payment.paid_at = now()
            payment.raw_response = intent
            payment.save()
            send_mail(
                subject="Payment Successful",
                message=f"Thank you for your payment of {payment.amount} {payment.currency}.",
                from_email="no-reply@myapp.com",
                recipient_list=[payment.user.email],
                fail_silently=True,
            )

        except Payment.DoesNotExist:
            logger.warning(f"Payment with transaction_id {transaction_id} not found.")

    elif event['type'] == 'payment_intent.payment_failed':
        intent = event['data']['object']
        transaction_id = intent.get('id')

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            payment.event_id = event_id
            payment.status = 'failed'
            payment.raw_response = intent
            payment.save()
        except Payment.DoesNotExist:
            logger.warning(f"Failed payment with transaction_id {transaction_id} not found.")

    return HttpResponse(status=200)
