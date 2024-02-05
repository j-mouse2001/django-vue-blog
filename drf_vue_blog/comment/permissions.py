from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    message = 'u must be the owner to update'

    def safe_method_or_owner(self, request, func):
        if request.method in permissions.SAFE_METHODS:
            return True
        return func()

    def has_permission(self, request, view):
        return self.safe_method_or_owner(
            request,
            lambda: request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return self.safe_method_or_owner(
            request,
            lambda: obj.author == request.user
        )
