# Generated by Django 2.1.7 on 2019-07-10 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0020_orderwithdeposit_order_info_with'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderwithdeposit',
            options={'verbose_name': '입금 연결', 'verbose_name_plural': '입금 연결'},
        ),
    ]
