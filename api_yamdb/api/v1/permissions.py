from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ только администраторам. Для остальных только для чтения."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """Доступ только администраторам, модераторам и авторам."""

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author
            )
        )


class IsAdminOrSuperUser(permissions.BasePermission):
    """Доступ администраторам и суперпользователям."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
            request.user.is_admin or
            request.user.is_superuser
        )
        )
