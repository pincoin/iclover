# Generated by Django 2.1.7 on 2019-10-30 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0050_auto_20191030_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainimg',
            name='origin_url',
            field=models.CharField(blank=True, max_length=255, verbose_name='샘플 url'),
        ),
    ]
