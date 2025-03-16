from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import Group

from .models import Account, Student, Teacher
from .serializers import AccountSerializer, GroupSerializer, StudentSerializer, TeacherSerializer
from .permissions import IsAdmin, IsTeacher, IsStudent


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Account.objects.all().order_by('-date_joined')
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Solo admin puede listar/ver usuarios
            permission_classes = [IsAdmin]
        elif self.action in ['update', 'partial_update']:  # Cada usuario puede editar su perfil
            permission_classes = [IsAuthenticated]
        elif (self.action == 'destroy') or (self.action == 'create'):
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Permitir GET a estudiantes y maestros
            permission_classes = [IsAuthenticated]
        else:  # Para PUT, POST, DELETE, solo los estudiantes pueden modificar su perfil
            permission_classes = [IsAuthenticated, IsStudent | IsAdmin]
        return [permission() for permission in permission_classes]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Permitir GET sin autenticación
            permission_classes = [AllowAny]  # Acceso libre a todos
        else:  # Para POST, PUT, DELETE, requiere ser maestro autenticado
            permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
        return [permission() for permission in permission_classes]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
