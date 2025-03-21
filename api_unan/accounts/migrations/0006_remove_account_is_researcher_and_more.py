# Generated by Django 5.1.6 on 2025-03-17 16:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_account_is_teacher_account_is_researcher_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_researcher',
        ),
        migrations.RemoveField(
            model_name='account',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='account',
            name='is_teacher',
            field=models.BooleanField(default=False, verbose_name='Es Docente'),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=50, verbose_name='Especialidad')),
                ('teacher_id', models.CharField(max_length=50, unique=True, verbose_name='Carnet de Docente')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Researcher',
        ),
    ]
