# Generated by Django 2.1.7 on 2019-05-13 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0008_auto_20190510_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='name',
            field=models.CharField(default=True, max_length=255, verbose_name='name of employees'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employees',
            name='state',
            field=models.BooleanField(default=True, verbose_name='state'),
        ),
    ]
