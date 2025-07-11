# apps/subscriptions/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.subscriptions.models import Subscription
from apps.subscriptions.serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

