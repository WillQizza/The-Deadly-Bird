# Generated by Django 5.0.1 on 2024-02-21 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0007_alter_inboxmessage_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='bio',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
