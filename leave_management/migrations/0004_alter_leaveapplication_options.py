# Generated by Django 4.2.6 on 2023-10-25 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave_management', '0003_rename_leave_type_leaveapplication_leave_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leaveapplication',
            options={'ordering': ['-id']},
        ),
    ]
