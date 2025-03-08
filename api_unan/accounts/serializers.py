from django.contrib.auth.models import Group
from django.template.context_processors import request
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Account, Student, Teacher

User = get_user_model()


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(required=True, validators=[])
    username = serializers.CharField(required=True, validators=[])
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = Account
        fields = ['url', 'email', 'username', 'first_name', 'last_name', 'password', 'telephone', 'description']

    def validate(self, data):
        request = self.context.get("request")
        print(f"Request: {request}")
        if request and request.method == "POST":
            # Para POST, se hace la validación normal.
            # Ejemplo: Verificar si el correo ya existe.
            if Account.objects.filter(email=data.get("email")).exists():
                raise serializers.ValidationError({"email": "Ya existe un usuario con este correo electrónico"})
        elif request and request.method in ["PUT", "PATCH"]:
            print("Validando PUT/PATCH")
            # Para PUT/PATCH, si se envía un correo, se permite que sea el mismo.
            if self.instance:
                email_nuevo = data.get("email", self.instance.email)
                if email_nuevo != self.instance.email:
                    raise serializers.ValidationError({"email": "No puede cambiar el correo electrónico"})
        return data

    def create(self, validated_data):
        print("Ejecutando create de AccountSerializer")
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user

    def update(self, instance, validated_data):
        print("Ejecutando update de AccountSerializer")
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        try:
            instance.save()
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return instance


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        account = Account.objects.create(**account_data, is_student=True)
        student = Student.objects.create(account=account, **validated_data)
        return student

    def update(self, instance, validated_data):
        account_data = validated_data.pop('account')
        if account_data:
            if 'email' in account_data:
                instance.account.email = account_data['email']
                instance.account.save()
            else:
                raise serializers.ValidationError('Solo se puede actualizar el correo electronico')
        return super().update(instance, validated_data)


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    account = AccountSerializer()
    teacher_id = serializers.CharField(required=True, validators=[])

    class Meta:
        model = Teacher
        fields = '__all__'

    def validate(self, data):
        request = self.context.get("request")
        print(f"Request: {request}")
        if request and request.method == "POST":
            # Para POST, se hace la validación normal.
            # Ejemplo: Verificar si el correo ya existe.
            if Teacher.objects.filter(teacher_id=data.get("teacher_id")).exists():
                raise serializers.ValidationError({"teacher_id": "Ya existe un docente con este ID"})
        elif request and request.method in ["PUT", "PATCH"]:
            print("Validando PUT/PATCH")
            # Para PUT/PATCH, si se envía un correo, se permite que sea el mismo.
            if self.instance:
                teacher_id_nuevo = data.get("teacher_id", self.instance.teacher_id)
                if teacher_id_nuevo != self.instance.teacher_id:
                    raise serializers.ValidationError({"teacher_id": "No puede cambiar el ID del docente"})
        return data

    def create(self, validated_data):
        print("Ejecutando create de TeacherSerializer")
        account_data = validated_data.pop('account')
        account = Account.objects.create(**account_data, is_teacher=True)
        teacher = Teacher.objects.create(account=account, **validated_data)
        return teacher

    def update(self, instance, validated_data):
        print("Ejecutando update de TeacherSerializer")
        account_data = validated_data.pop('account', None)
        if account_data:
            # Actualizamos la cuenta existente usando un serializer parcial
            account_serializer = AccountSerializer(instance.account, data=account_data, partial=True)
            account_serializer.is_valid(raise_exception=True)
            account_serializer.save()
        # Actualizamos los demás campos del docente
        return super().update(instance, validated_data)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
