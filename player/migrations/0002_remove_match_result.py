# Generated by Django 3.2.13 on 2022-06-27 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='result',
        ),
    ]