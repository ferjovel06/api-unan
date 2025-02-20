from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import Account, Student, Teacher


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'email', 'username', 'first_name', 'last_name']


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        account = Account.objects.create(**account_data)
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
        return teacher


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']