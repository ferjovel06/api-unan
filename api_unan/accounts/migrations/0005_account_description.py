# Generated by Django 5.1.6 on 2025-02-20 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_account_telephone'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='description',
            field=models.TextField(default='', max_length=500, verbose_name='Descripcion'),
        ),
    ]
