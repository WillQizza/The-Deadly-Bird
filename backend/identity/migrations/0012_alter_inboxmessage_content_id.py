# Generated by Django 5.0.1 on 2024-02-27 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0011_alter_author_id_alter_inboxmessage_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inboxmessage',
            name='content_id',
            field=models.CharField(max_length=255),
        ),
    ]
