# Generated by Django 4.2.6 on 2023-10-18 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_management', '0008_alter_leaveapplication_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restricteddays',
            name='day_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]