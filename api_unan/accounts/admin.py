from django.contrib import admin
from .models import Account, Student, Teacher


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_admin', 'is_active', 'is_superuser')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_admin', 'is_active', 'is_superuser')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('career', 'year_in_course', 'student_id')
    search_fields = ('career', 'year_in_course', 'student_id')
    list_filter = ('career', 'year_in_course')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('specialization', 'teacher_id')
    search_fields = ('specialization', 'teacher_id')
    list_filter = ('specialization',)
