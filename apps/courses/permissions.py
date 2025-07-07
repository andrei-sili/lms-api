# apps/courses/permissions.py

from rest_framework import permissions


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
