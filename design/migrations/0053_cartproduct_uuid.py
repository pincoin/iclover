# Generated by Django 2.1.7 on 2019-11-08 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0052_auto_20191103_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='uuid',
            field=models.CharField(default='d1792c2daf', max_length=15),
        ),
    ]
