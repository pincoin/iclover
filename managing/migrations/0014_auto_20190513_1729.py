# Generated by Django 2.1.7 on 2019-05-13 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0013_employees_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='group',
            field=models.IntegerField(choices=[(0, '관리자'), (1, '디자이너'), (2, '알바'), (3, '기타')], db_index=True, default=1, verbose_name='그룹선택'),
        ),
    ]
