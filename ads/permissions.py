from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # allow anyone to get, head and options
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.user != request.user:
            raise PermissionDenied(detail="Вы не являетесь создателем этого объявления и не можете его изменять.")
        return True
