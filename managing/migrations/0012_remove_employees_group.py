# Generated by Django 2.1.7 on 2019-05-13 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0011_auto_20190513_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employees',
            name='group',
        ),
    ]
