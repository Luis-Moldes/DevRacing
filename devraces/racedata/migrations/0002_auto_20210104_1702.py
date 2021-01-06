# Generated by Django 3.1.4 on 2021-01-04 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racedata', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pilot',
            options={'ordering': ['total_pts']},
        ),
        migrations.AddField(
            model_name='pilot',
            name='total_pts',
            field=models.IntegerField(default=0),
        ),
    ]
