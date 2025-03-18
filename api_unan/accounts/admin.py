from django.contrib import admin
from .models import Account, Student, Teacher, Career, KnowledgeArea


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'career', 'is_admin', 'is_active', 'is_student', 'is_teacher')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'career')
    list_filter = ('career', 'is_admin', 'is_active', 'is_superuser')

    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.set_password(obj.password)
        obj.save()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('account', 'year_in_course', 'student_id')
    search_fields = ('account', 'year_in_course', 'student_id')
    list_filter = ('account', 'year_in_course')
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
    list_display = ('account', 'teacher_id')
    search_fields = ('account', 'teacher_id')
    raw_id_fields = ['account']

    def save_model(self, request, obj, form, change):
        obj.account.is_student = False
        obj.account.is_teacher = True
        obj.account.is_active = True

        if obj.account.password:
            obj.account.set_password(obj.account.password)

        obj.account.save()
        super().save_model(request, obj, form, change)

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'knowledge_area', 'department')
    search_fields = ('name', 'knowledge_area', 'department')

@admin.register(KnowledgeArea)
class KnowledgeAreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)