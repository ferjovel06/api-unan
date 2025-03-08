from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """
    Permite a los estudiantes ver y editar su propia información
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_student:
            if request.method in permissions.SAFE_METHODS:
                return obj == request.user
            elif request.method == "PUT":
                return obj == request.user and "email" in request.data
        return False


class IsTeacher(permissions.BasePermission):
    """
    Permite a los docentes ver todos los perfiles y editar su propia información.
    No permite que los docentes realicen POST ni DELETE.
    """
    def has_permission(self, request, view):
        print("Verificando permisos de maestro")
        # Permitir GET, HEAD, OPTIONS y PUT, pero bloquear POST y DELETE
        return request.user.is_teacher and request.method in permissions.SAFE_METHODS + ("PUT",)

    def has_object_permission(self, request, view, obj):
        if request.user.is_teacher:
            if request.method in permissions.SAFE_METHODS:
                return True  # Puede ver cualquier perfil
            elif request.method == "PUT":
                print("Verificando si el maestro puede editar el perfil")
                print(obj.account==request.user)
                return obj.account == request.user  # Solo puede editar su propio perfil
        return False


class IsAdmin(permissions.BasePermission):
    """
    Permite acceso total a los administradores
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin or request.user.is_superuser or request.user.is_staff
