# Generated by Django 5.1.6 on 2025-02-20 02:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=50, verbose_name='Apellido')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Nombre de Usuario')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Correo Electronico')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('career', models.CharField(max_length=50, verbose_name='Carrera')),
                ('year_in_course', models.IntegerField(default=1, verbose_name='Año en Curso')),
                ('student_id', models.CharField(max_length=50, verbose_name='Carnet de Estudiante')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=50, verbose_name='Especialidad')),
                ('teacher_id', models.CharField(max_length=50, verbose_name='Carnet de Docente')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
