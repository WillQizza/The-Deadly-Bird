# Generated by Django 5.0.1 on 2024-02-03 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0002_author_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='username',
        ),
    ]
