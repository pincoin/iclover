# Generated by Django 2.1.7 on 2019-09-30 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0022_customerorderproduct_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorderproduct',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='품목 종류 title'),
        ),
        migrations.AlterField(
            model_name='customerorderproduct',
            name='kind',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='품목 종류 kind'),
        ),
    ]
