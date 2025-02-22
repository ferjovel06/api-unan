from rest_framework import permissions


class IsAdminToDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permitir GET, POST, PUT para todos, pero DELETE solo para admins
        if request.method == "DELETE":
            return request.user.is_admin
        return True
