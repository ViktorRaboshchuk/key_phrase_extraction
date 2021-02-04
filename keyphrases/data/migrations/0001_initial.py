# Generated by Django 3.1.6 on 2021-02-03 16:09

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_area', models.TextField(max_length=150000)),
            ],
        ),
        migrations.CreateModel(
            name='KeyPhrases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrases', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='', max_length=25500), default=list, size=None), size=None)),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.text')),
            ],
        ),
    ]
