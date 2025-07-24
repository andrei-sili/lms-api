# apps/payments/serializers.py
from decimal import Decimal

from rest_framework import serializers
from apps.payments.models import Payment
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'amount',
            'currency',
            'status',
            'method',
            'transaction_id',
            'paid_at',
            'created_at',
            'updated_at',
            'provider',
            'raw_response',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'transaction_id', 'raw_response', 'paid_at',
                            'status']

    def validate_amount(self, value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Amount must be greater than 0.00.")
        return value

    def validate_currency(self, value):
        allowed_currencies = ['EUR', 'USD']
        if value not in allowed_currencies:
            raise serializers.ValidationError(f"Currency must be one of: {', '.join(allowed_currencies)}")
        return value

    def validate_method(self, value):
        allowed_methods = [choice[0] for choice in Payment.Method.choices]
        if value not in allowed_methods:
            raise serializers.ValidationError(f"Method must be one of: {', '.join(allowed_methods)}")
        return value

    def validate(self, attrs):
        method = attrs.get('method')
        provider = attrs.get('provider')

        if provider and provider != method:
            raise serializers.ValidationError("Provider must match the selected payment method.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        amount = validated_data['amount']
        currency = validated_data.get('currency', 'EUR')
        method = validated_data.get('method')

        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency=currency.lower(),
            payment_method_types=[method],
            description=f"Payment by {user.email}",
            metadata={'user_id': user.id}
        )

        payment = Payment.objects.create(
            user=user,
            amount=amount,
            currency=currency,
            method=method,
            provider='stripe',
            transaction_id=intent['id'],
            status='pending',
            raw_response=intent
        )

        return payment

