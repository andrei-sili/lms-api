# apps/payments/models.py

from django.db import models
from apps.users.models import User


class Payment(models.Model):
    class Method(models.TextChoices):
        CARD = 'card', 'Credit/Debit Card'
        PAYPAL = 'paypal', 'PayPal'
        STRIPE = 'stripe', 'Stripe'
        BANK = 'bank_transfer', 'Bank Transfer'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'
        CANCELED = 'canceled', 'Canceled'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EUR')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    method = models.CharField(max_length=20, choices=Method.choices)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    event_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    provider = models.CharField(max_length=50, blank=True, null=True)
    raw_response = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.currency} [{self.status}]"


