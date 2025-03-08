from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Account, Student, Teacher

User = get_user_model()


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'email', 'username', 'first_name', 'last_name', 'password', 'telephone', 'description']
        extra_kwargs = {
            'password': {'write_only': True}
        }

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

        instance.save()
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

    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        print("Ejecutando create de TeacherSerializer")
        account_data = validated_data.pop('account')
        account = Account.objects.create(**account_data, is_teacher=True)
        teacher = Teacher.objects.create(account=account, **validated_data)
        return teacher


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
