# Generated by Django 2.1.7 on 2019-10-16 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0041_auto_20191016_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorderinfo',
            name='tax_bool',
            field=models.BooleanField(default=True),
        ),
    ]
