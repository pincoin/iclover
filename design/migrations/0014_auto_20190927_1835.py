# Generated by Django 2.1.7 on 2019-09-27 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0013_auto_20190927_1751'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productpriceapi',
            old_name='size',
            new_name='size_book',
        ),
    ]
