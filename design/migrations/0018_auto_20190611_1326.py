# Generated by Django 2.1.7 on 2019-06-11 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0017_auto_20190611_0032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderinfo',
            old_name='manager',
            new_name='fix_manager',
        ),
    ]