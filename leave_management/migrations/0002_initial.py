# Generated by Django 4.2.6 on 2023-10-22 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('leave_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveapplication',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager_leave_requests', to='user.adminmanagement'),
        ),
    ]
