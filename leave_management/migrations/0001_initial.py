# Generated by Django 4.2.6 on 2023-10-15 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.CharField(blank=True, max_length=30, null=True)),
                ('leave_type', models.CharField(choices=[('VACATION', 'VACATION'), ('SICK_LEAVE', 'SICK_LEAVE'), ('MATERNITY_LEAVE', 'MATERNITY_LEAVE')], max_length=15)),
                ('duration_type', models.CharField(choices=[('FULL_DAY', 'FULL_DAY'), ('HALF_DAY', 'HALF_DAY')], max_length=10)),
                ('leave_status', models.CharField(choices=[('APPROVE', 'APPROVE'), ('REJECT', 'REJECT')], max_length=7)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RestrictedDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_name', models.CharField(max_length=50)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='LeavePolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_leave_per_year', models.PositiveIntegerField()),
                ('unpaid_leave_cost_per_day', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid_leave_taken', models.PositiveIntegerField(default=0)),
                ('unpaid_leave_taken', models.PositiveIntegerField(default=0)),
                ('leave_for_all_employees', models.BooleanField(default=False)),
                ('max_leaves_per_month', models.PositiveIntegerField()),
                ('restricted_days_of_week', models.ManyToManyField(blank=True, to='leave_management.restricteddays')),
            ],
        ),
    ]