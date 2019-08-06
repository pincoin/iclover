# Generated by Django 2.1.7 on 2019-08-06 09:26

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0004_auto_20190806_1802'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('_tree_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sectorscategory',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sectorscategory',
            name='slug',
            field=models.IntegerField(default=0),
        ),
    ]
