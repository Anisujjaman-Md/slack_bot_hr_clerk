# Generated by Django 4.2.6 on 2023-10-22 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('leave_management', '0002_initial'),
        ('user', '0002_adminmanagement_manager'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AdminManagement',
            new_name='User',
        ),
    ]
