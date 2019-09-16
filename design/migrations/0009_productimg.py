# Generated by Django 2.1.7 on 2019-09-11 11:30

import design.models
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0008_orderimg_employees'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='slug')),
                ('keyword', models.CharField(blank=True, max_length=255, verbose_name='키워드')),
                ('images', models.ImageField(blank=True, null=True, upload_to=design.models.ProductImg.upload_to_product_default_img, verbose_name='product_default_img')),
            ],
            options={
                'verbose_name': '기본 이미지',
                'verbose_name_plural': '기본 이미지',
            },
        ),
    ]