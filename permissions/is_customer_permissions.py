from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    message = "Please login as a customer"

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "role", None) != "customer":
            return False
        return True
