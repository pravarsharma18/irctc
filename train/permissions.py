from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated


class CreatePermission(BasePermission):
    message = 'You are not allowed to Create Books.'

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_superuser
        )
