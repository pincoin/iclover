# Generated by Django 2.1.7 on 2019-10-15 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0036_auto_20191015_1413'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productpriceapi',
            old_name='buy_pricie',
            new_name='buy_price',
        ),
    ]
