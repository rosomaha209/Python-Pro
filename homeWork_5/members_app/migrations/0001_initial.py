# Generated by Django 5.0.1 on 2024-02-17 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('courses', models.ManyToManyField(to='courses_app.course')),
            ],
        ),
    ]
