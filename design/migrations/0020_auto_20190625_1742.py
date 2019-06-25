# Generated by Django 2.1.7 on 2019-06-25 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0019_auto_20190622_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='state',
            field=models.IntegerField(blank=True, choices=[(0, '견적'), (1, '주문'), (2, '시안'), (3, '제작'), (4, '완료'), (5, '취소'), (6, '보류'), (7, '환불'), (8, '입금대기')], db_index=True, default=0, verbose_name='상태값'),
        ),
    ]
