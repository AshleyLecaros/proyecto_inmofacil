# Generated by Django 4.2.11 on 2024-06-10 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmofacil_app', '0005_rename_mail_usuario_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='direccion_id',
        ),
    ]
