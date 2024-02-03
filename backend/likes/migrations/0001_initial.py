# Generated by Django 5.0.1 on 2024-02-03 20:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('identity', '0001_initial'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='identity.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
    ]
