from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Доступ для администраторов"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="Администраторы").exists()


class IsTeacher(permissions.BasePermission):
    """Доступ для преподавателей"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="Преподаватели").exists()


class IsStudent(permissions.BasePermission):
    """Доступ для студентов"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="Студенты").exists()
