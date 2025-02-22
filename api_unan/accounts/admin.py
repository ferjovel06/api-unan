from django.contrib import admin
from .models import Account, Student, Teacher


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_admin', 'is_active', 'is_superuser')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_admin', 'is_active', 'is_superuser')

    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.set_password(obj.password)
        obj.save()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('account', 'career', 'year_in_course', 'student_id')
    search_fields = ('account', 'career', 'year_in_course', 'student_id')
    list_filter = ('account', 'career', 'year_in_course')
    raw_id_fields = ['account']

    def save_model(self, request, obj, form, change):
        obj.account.is_student = True
        obj.account.is_teacher = False
        obj.account.is_active = True

        if obj.account.password:
            obj.account.set_password(obj.account.password)

        obj.account.save()
        super().save_model(request, obj, form, change)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('account', 'specialization', 'teacher_id')
    search_fields = ('account', 'specialization', 'teacher_id')
    list_filter = ('specialization',)
    raw_id_fields = ['account']

    def save_model(self, request, obj, form, change):
        obj.account.is_student = False
        obj.account.is_teacher = True
        obj.account.is_active = True

        if obj.account.password:
            obj.account.set_password(obj.account.password)

        obj.account.save()
        super().save_model(request, obj, form, change)
