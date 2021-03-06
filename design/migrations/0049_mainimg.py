# Generated by Django 2.1.7 on 2019-10-30 05:35

import design.models
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0048_deliveryprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name of product')),
                ('active', models.BooleanField(default=True)),
                ('banner_img', models.ImageField(blank=True, upload_to=design.models.MainImg.upload_to_product, verbose_name='banner_img')),
            ],
            options={
                'verbose_name': '메인 배너',
                'verbose_name_plural': '메인 배너',
            },
        ),
    ]
