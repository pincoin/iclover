# Generated by Django 2.1.7 on 2019-10-15 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0035_auto_20191015_1409'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productpriceapi',
            old_name='buy',
            new_name='buy_pricie',
        ),
    ]