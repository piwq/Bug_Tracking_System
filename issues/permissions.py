from rest_framework import permissions


class IsQAOrReadOnly(permissions.BasePermission):
    """
    QA могут создавать и редактировать.
    Остальные (Разработчики) могут только смотреть.
    """

    def has_permission(self, request, view):
        # Безопасные методы (GET, HEAD, OPTIONS) разрешены всем авторизованным
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Изменять данные (POST, PUT, DELETE) могут только QA или Админы
        return request.user.is_authenticated and (request.user.role == 'QA' or request.user.is_superuser)


class IsReporterOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактировать баг только тому, кто его создал (или админу).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reporter == request.user or request.user.is_superuser