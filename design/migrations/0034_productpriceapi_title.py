# Generated by Django 2.1.7 on 2019-10-14 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0033_customerorderinfo_show_memo'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpriceapi',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='품목 종류 한글'),
        ),
    ]
