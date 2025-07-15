# apps/lessons/permissions.py

from apps.courses.models import Enrollment
from apps.lessons.models import Lesson
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEnrolledInLessonCourse(BasePermission):
    """
    Allow action only if the user is enrolled in the lesson's course.
    """

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        lesson_id = request.data.get('lesson')
        if not lesson_id:
            return False

        try:
            lesson = Lesson.objects.select_related('course').get(id=lesson_id)
        except Lesson.DoesNotExist:
            return False

        return Enrollment.objects.filter(
            user=request.user,
            course=lesson.course
        ).exists()


class IsCommentOwner(BasePermission):
    """
    - SAFE_METHODS (GET, HEAD, OPTIONS): all user
    - POST (create): all users
    - PUT/PATCH/DELETE:  comment owner
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.method == 'POST'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwnerOfProgress(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

