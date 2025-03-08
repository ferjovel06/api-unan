from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, telephone, username, description, password, is_student=False, is_teacher=False):
        if not email:
            raise ValidationError('El usuario debe tener un correo electronico')
        if not username:
            raise ValidationError('El usuario debe tener un nombre de usuario')

        if is_student and is_teacher:
            raise ValidationError('Un usuario no puede ser estudiante y docente al mismo tiempo')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            telephone=telephone,
            description=description
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, telephone, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            telephone=telephone,
            description='Administrador'
        )

        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField('Nombre', max_length=50, null=True, blank=True)
    last_name = models.CharField('Apellido', max_length=50, null=True, blank=True)
    username = models.CharField('Nombre de Usuario', max_length=50, unique=True)
    email = models.EmailField('Correo Electronico', max_length=100, unique=True)
    telephone = models.CharField('Telefono', max_length=15, null=True, blank=True)
    description = models.TextField('Descripcion', max_length=500, null=True, blank=True)

    # Atributos de django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Atributos de la aplicacion
    is_student = models.BooleanField('Es Estudiante', default=False)
    is_teacher = models.BooleanField('Es Docente', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'telephone']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return self.is_admin or self.is_staff

    def clean(self):
        self.email = self.__class__.objects.normalize_email(self.email)
        if self.is_student and self.is_teacher:
            raise ValidationError('Un usuario no puede ser estudiante y docente al mismo tiempo')


class Student(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='student_profile')
    career = models.CharField('Carrera', max_length=50)
    year_in_course = models.IntegerField('Año en Curso', default=1)
    student_id = models.CharField('Carnet de Estudiante', max_length=50, unique=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.account.first_name} {self.account.last_name} - Estudiante"

    def clean(self):
        if self.year_in_course < 1:
            raise ValidationError('El año en curso no puede ser menor a 1')
        if self.year_in_course > 5:
            raise ValidationError('El año en curso no puede ser mayor a 5')
        if Teacher.objects.filter(account=self.account).exists():
            raise ValidationError('Este usuario ya esta registrado como docente')


class Teacher(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='teacher_profile')
    specialization = models.CharField('Especialidad', max_length=50)
    teacher_id = models.CharField('Carnet de Docente', max_length=50, unique=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.account.first_name} {self.account.last_name} - Docente"

    def clean(self):
        if Student.objects.filter(account=self.account).exists():
            raise ValidationError('Este usuario ya esta registrado como estudiante')
