from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import Group

from .models import Account, Student, Teacher, Career, KnowledgeArea
from .serializers import AccountSerializer, GroupSerializer, StudentSerializer, TeacherSerializer, CareerSerializer, KnowledgeAreaSerializer
from .permissions import IsAdmin, IsTeacher, IsStudent

from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


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


class CareerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows careers to be viewed or edited.
    """
    queryset = Career.objects.all().order_by('name')
    serializer_class = CareerSerializer
    permission_classes = [IsAuthenticated]


class KnowledgeAreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows knowledge areas to be viewed or edited.
    """
    queryset = KnowledgeArea.objects.all().order_by('name')
    serializer_class = KnowledgeAreaSerializer
    permission_classes = [IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenBlacklistResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenBlacklistResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
