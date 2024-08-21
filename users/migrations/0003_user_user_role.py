# Generated by Django 5.0.4 on 2024-06-01 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_jobs'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_role',
            field=models.CharField(choices=[('student', 'student'), ('teacher', 'teacher'), ('admin', 'admin')], default=1, max_length=100),
            preserve_default=False,
        ),
    ]
