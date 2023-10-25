# Generated by Django 4.2.6 on 2023-10-25 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SlackUserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=255)),
                ('team_id', models.CharField(max_length=255)),
                ('deleted', models.BooleanField()),
                ('real_name', models.CharField(max_length=255)),
                ('is_admin', models.BooleanField()),
                ('is_owner', models.BooleanField()),
                ('is_primary_owner', models.BooleanField()),
                ('is_restricted', models.BooleanField()),
                ('is_ultra_restricted', models.BooleanField()),
                ('is_bot', models.BooleanField()),
            ],
        ),
    ]