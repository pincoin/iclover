# Generated by Django 2.1.11 on 2019-12-12 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0005_auto_20191021_0433'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='aspect',
            field=models.IntegerField(choices=[(0, '가로'), (1, '세로')], default=0, verbose_name='가로 / 세로'),
        ),
    ]
