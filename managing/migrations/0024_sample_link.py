# Generated by Django 2.1.7 on 2019-07-16 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0023_auto_20190716_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='link',
            field=models.CharField(blank=True, max_length=255, verbose_name='링크 url'),
        ),
    ]
