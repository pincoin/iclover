# Generated by Django 2.1.7 on 2019-04-23 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ask',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='deposit',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employees',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sample',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
    ]
