from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
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
        elif self.action == 'destroy':  # Solo admin puede eliminar usuarios
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsStudent]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsTeacher]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
