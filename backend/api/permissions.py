from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """ Разрешение на создание или редоктирование только для автора.
    Остальные только чтение"""

    def has_permission(self, request, view) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return request.user.is_superuser or obj.author == request.user
        return False
