# Generated by Django 5.0.1 on 2024-02-03 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0005_inboxmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inboxmessage',
            name='content_type',
            field=models.CharField(choices=[], max_length=50),
        ),
    ]
