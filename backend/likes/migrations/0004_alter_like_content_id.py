# Generated by Django 5.0.1 on 2024-02-22 22:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("likes", "0003_rename_post_like_content_id_like_content_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="like",
            name="content_id",
            field=models.CharField(max_length=10),
        ),
    ]