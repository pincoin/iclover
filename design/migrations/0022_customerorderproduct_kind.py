# Generated by Django 2.1.7 on 2019-09-30 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0021_auto_20190930_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorderproduct',
            name='kind',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='품목 종류'),
        ),
    ]
