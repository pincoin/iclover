# Generated by Django 2.1.7 on 2019-10-04 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('managing', '0002_remove_sample_images_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerMemo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('keyword', models.CharField(blank=True, max_length=255, null=True, verbose_name='키워드')),
                ('manager', models.CharField(blank=True, max_length=255, null=True, verbose_name='담당자')),
                ('memo', models.CharField(blank=True, max_length=255, null=True, verbose_name='메모')),
                ('confirm', models.CharField(blank=True, max_length=255, null=True, verbose_name='시안 확인')),
                ('hoo', models.CharField(blank=True, max_length=255, null=True, verbose_name='후가공')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '고객 프로필 추가정보 using inside',
                'verbose_name_plural': '고객 프로필 추가정보 using inside',
            },
        ),
    ]
