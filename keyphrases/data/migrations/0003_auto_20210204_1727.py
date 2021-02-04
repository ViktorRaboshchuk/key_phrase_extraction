# Generated by Django 3.1.6 on 2021-02-04 14:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_keyphrases_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyphrases',
            name='time',
        ),
        migrations.AddField(
            model_name='text',
            name='time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
