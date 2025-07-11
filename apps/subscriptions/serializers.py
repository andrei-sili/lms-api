# apps/subscriptions/serializers.py

from rest_framework import serializers

from apps.subscriptions.models import Subscription
from django.utils import timezone


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'id',
            'user',
            'start_date',
            'end_date',
            'amount',
            'is_active',
        ]
        read_only_fields = ['id', 'user', 'start_date', 'is_active']

    def validate(self, data):
        start_date = self.instance.start_date if self.instance else timezone.now()
        end_date = data.get('end_date')

        if end_date and end_date <= start_date:
            raise serializers.ValidationError("End date must be after start date.")

        amount = data.get('amount')
        if amount is not None and amount <= 0:
            raise serializers.ValidationError("Amount must be a positive value.")

        if Subscription.objects.filter(user=self.context['request'].user, is_active=True).exists():
            raise serializers.ValidationError("User already has an active subscription.")

        return data
