from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, telephone, username, description, password):
        if not email:
            raise ValueError('El usuario debe tener un correo electronico')
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')

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
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField('Nombre', max_length=50)
    last_name = models.CharField('Apellido', max_length=50)
    username = models.CharField('Nombre de Usuario', max_length=50, unique=True)
    email = models.EmailField('Correo Electronico', max_length=100, unique=True)
    telephone = models.CharField('Telefono', max_length=15)
    description = models.TextField('Descripcion', max_length=500, null=True, blank=True)

    # Atributos de django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'telephone']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Student(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    career = models.CharField('Carrera', max_length=50)
    year_in_course = models.IntegerField('Año en Curso', default=1)
    student_id = models.CharField('Carnet de Estudiante', max_length=50)

    objects = models.Manager()

    def __str__(self):
        return f"{self.account.first_name} {self.account.last_name} - Estudiante"


class Teacher(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    specialization = models.CharField('Especialidad', max_length=50)
    teacher_id = models.CharField('Carnet de Docente', max_length=50)

    objects = models.Manager()

    def __str__(self):
        return f"{self.account.first_name} {self.account.last_name} - Docente"
