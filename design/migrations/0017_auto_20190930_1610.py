# Generated by Django 2.1.7 on 2019-09-30 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0016_customerorderinfo_customerorderproduct'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerorderinfo',
            old_name='name',
            new_name='company',
        ),
    ]
