# Generated by Django 5.0.1 on 2024-02-22 18:53

import deadlybird.util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('following', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='following',
            name='id',
            field=models.CharField(default=deadlybird.util.generate_next_id, max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='followingrequest',
            name='id',
            field=models.CharField(default=deadlybird.util.generate_next_id, max_length=10, primary_key=True, serialize=False),
        ),
    ]
