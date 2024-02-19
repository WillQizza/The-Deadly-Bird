# Generated by Django 5.0.1 on 2024-02-18 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0006_alter_inboxmessage_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inboxmessage',
            name='content_type',
            field=models.CharField(choices=[('post', 'Post'), ('follow', 'Follow'), ('like', 'Like'), ('comment', 'Comment')], max_length=50),
        ),
    ]