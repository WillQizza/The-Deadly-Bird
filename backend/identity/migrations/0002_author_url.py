# Generated by Django 5.0.1 on 2024-02-03 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='url',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]