from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Account, Student, Teacher


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'email', 'username', 'first_name', 'last_name', 'password', 'telephone', 'description']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
        return super().update(instance, validated_data)


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        account = Account.objects.create(**account_data)
        account.is_student = True
        student = Student.objects.create(account=account, **validated_data)
        return student


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        account = Account.objects.create(**account_data)
        teacher = Teacher.objects.create(account=account, **validated_data)
        account.is_teacher = True
        return teacher


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']