# apps/lessons/permissions.py

from rest_framework.permissions import BasePermission
from apps.courses.models import Enrollment
from apps.lessons.models import Lesson


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
