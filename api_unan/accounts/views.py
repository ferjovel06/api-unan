from rest_framework import viewsets, permissions
from django.contrib.auth.models import Group

from .models import Account, Student, Teacher
from .serializers import AccountSerializer, GroupSerializer, StudentSerializer, TeacherSerializer
from .permissions import IsAdminToDelete


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Account.objects.all().order_by('-date_joined')
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminToDelete]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Account.objects.all().order_by('-date_joined')
        return Account.objects.filter(id=user.id).order_by('-date_joined')



class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
