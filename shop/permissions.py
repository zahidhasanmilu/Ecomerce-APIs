from rest_framework import permissions
from rest_framework.permissions import BasePermission

# --------------- Is Owner Or Read Only ---------------#
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.owner == request.user

# --------------- Is Shop Owner Role ---------------#
class IsShopOwnerRole(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_authenticated and request.user.role == "shop_owner"
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH"]:
            return (
                request.user.is_authenticated
                and request.user.role == "shop_owner"
                and obj.owner == request.user
            )
        return True
