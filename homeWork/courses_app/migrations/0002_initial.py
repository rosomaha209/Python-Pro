# Generated by Django 5.0.2 on 2024-02-25 09:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses_app', '0001_initial'),
        ('members_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='users',
            field=models.ManyToManyField(through='members_app.UserEnrollment', to=settings.AUTH_USER_MODEL),
        ),
    ]
