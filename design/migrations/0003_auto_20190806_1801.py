# Generated by Django 2.1.7 on 2019-08-06 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0002_auto_20190806_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sectorscategory',
            name='slug',
            field=models.IntegerField(default=0),
        ),
    ]
