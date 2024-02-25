# Generated by Django 5.0.1 on 2024-02-23 23:24

import deadlybird.util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_comment_id_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.CharField(default=deadlybird.util.generate_next_id, max_length=255, primary_key=True, serialize=False),
        ),
    ]