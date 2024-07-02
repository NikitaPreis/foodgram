from rest_framework import permissions


class UserSelfAccess(permissions.BasePermission):
    """Разрешения для владельца профиля.

    Просмотр и изменение данных профиля."""

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class AdminAccess(permissions.BasePermission):
    """Разрешения для администратора и суперпользователя."""

    def has_permission(self, request, view):
        return request.user.is_admin


class AuthorOrAdminOrReadOnlyAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class AuthorOrAdminAccess(permissions.BasePermission):
    """Разрешения для автора, модератора и администратора."""

    def has_object_permission(self, request, view, obj):
        return ((request.user.is_authenticated
                and (request.user.is_admin
                     or request.user == obj.author))
                or request.method in permissions.SAFE_METHODS)


class AdminOrReadOnlyAccess(permissions.BasePermission):
    """Разрешение для администратора или доступ к чтению"""

    def has_permission(self, request, view):
        return (request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class UserPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class UserProfilePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class UserAvatarPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class SubscriptionAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class AuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class RecipeSerializer(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user.username
