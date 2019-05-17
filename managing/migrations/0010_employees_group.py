# Generated by Django 2.1.7 on 2019-05-13 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0009_auto_20190513_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='group',
            field=models.IntegerField(choices=[(0, '관리자'), (1, '직원'), (2, '알바'), (3, '기타')], db_index=True, default=1, verbose_name='그룹선택'),
            preserve_default=False,
        ),
    ]
