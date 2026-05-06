from rest_framework import permissions


# ---------------Is User Logged Out ---------------#
class IsLoggedOut(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


# ---------------Is Owner Or Read Only ---------------#
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user and request.user.is_authenticated
