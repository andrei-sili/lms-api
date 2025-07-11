# apps/subscriptions/models.py

from django.db import models
from apps.users.models import User


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - Active: {self.is_active}"