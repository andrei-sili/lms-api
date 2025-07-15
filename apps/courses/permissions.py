# apps/courses/permissions.py

from rest_framework import permissions
from rest_framework.permissions import BasePermission

from apps.subscriptions.models import Subscription


class IsOwnerTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if request.method == "POST":
            return request.user and request.user.is_authenticated and request.user.role == "teacher"
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
                request.user
                and request.user.is_authenticated
                and request.user.role == "teacher"
                and obj.teacher == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_staff


class HasActiveSubscription(BasePermission):
    message = "You need an active subscription"

    def has_permission(self, request, view):
        user = request.user
        return Subscription.objects.filter(user=user, status='active').exists()


class IsCertificateOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
