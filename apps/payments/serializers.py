# apps/payments/serializers.py
from decimal import Decimal

from rest_framework import serializers
from apps.payments.models import Payment


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
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'transaction_id', 'raw_response', 'paid_at', 'status']

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
        return super().create(validated_data)

