from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStudent(BasePermission):
    """
    Permite a los estudiantes ver y editar su propia información
    """

    def has_permission(self, request, view):
        print("Verificando permisos de estudiante")
        # Permitir GET, HEAD, OPTIONS y PUT, pero bloquear POST y DELETE
        return request.user.is_student and request.method in SAFE_METHODS + ("PUT",)

    def has_object_permission(self, request, view, obj):
        if request.user.is_student:
            if request.method == "PUT":
                return obj == request.user and "email" in request.data
        return False


class IsTeacher(BasePermission):
    """
    Permite a los docentes ver todos los perfiles y editar su propia información.
    No permite que los docentes realicen POST ni DELETE.
    """
    def has_permission(self, request, view):
        print("Verificando permisos de maestro")
        # Permitir GET, HEAD, OPTIONS y PUT, pero bloquear POST y DELETE
        return request.user.is_teacher and request.method in SAFE_METHODS + ("PUT",)

    def has_object_permission(self, request, view, obj):
        if request.user.is_teacher:
            if request.method == "PUT":
                print("Verificando si el maestro puede editar el perfil")
                print(obj.account==request.user)
                return obj.account == request.user  # Solo puede editar su propio perfil
        return False


class IsAdmin(BasePermission):
    """
    Permite acceso total a los administradores
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin or request.user.is_superuser or request.user.is_staff
