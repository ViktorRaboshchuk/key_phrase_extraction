# Generated by Django 3.1.6 on 2021-02-04 14:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyphrases',
            name='time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]