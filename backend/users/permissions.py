from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Только владелец может просматривать свои данные."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.id == int(
            request.parser_context["kwargs"]["id"]
        )
