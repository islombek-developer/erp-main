# Generated by Django 5.0.4 on 2024-05-30 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='jobs',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
