# Generated by Django 3.1 on 2021-05-05 01:23

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210502_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, null=True, size=None),
        ),
    ]
