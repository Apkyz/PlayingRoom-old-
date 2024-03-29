# Generated by Django 3.2.13 on 2022-07-08 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('descr', models.CharField(max_length=500)),
                ('stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('items', models.ManyToManyField(to='cashregister.Item')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.player')),
            ],
        ),
    ]
