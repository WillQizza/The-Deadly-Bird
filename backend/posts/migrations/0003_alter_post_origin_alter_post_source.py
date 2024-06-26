# Generated by Django 5.0.1 on 2024-02-03 20:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0001_initial'),
        ('posts', '0002_alter_comment_content_type_alter_post_content_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='origin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nodes.node'),
        ),
    ]
