from django.contrib import admin
from .models import Account, Student, Teacher


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_admin', 'is_active', 'is_superuser')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_admin', 'is_active', 'is_superuser')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('account', 'career', 'year_in_course', 'student_id')
    search_fields = ('account', 'career', 'year_in_course', 'student_id')
    list_filter = ('account', 'career', 'year_in_course')
    raw_id_fields = ['account']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('account', 'specialization', 'teacher_id')
    search_fields = ('account', 'specialization', 'teacher_id')
    list_filter = ('specialization',)
    raw_id_fields = ['account']
