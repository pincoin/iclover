# Generated by Django 2.1.7 on 2019-09-27 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0014_auto_20190927_1835'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productpriceapi',
            old_name='size_book',
            new_name='size',
        ),
    ]
