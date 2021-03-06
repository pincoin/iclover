# Generated by Django 2.1.7 on 2019-10-10 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_auto_20190920_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='주소'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='address2',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='주소2'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='address_detail',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='상세주소'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='address_option',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='주소 참고'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='business',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='업태'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='ceo',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='대표자명'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='company',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='업체명'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='memo',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='메모'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='sectors',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='업종'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='tax_bill_mail',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='이메일'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='tell',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='매장번호'),
        ),
    ]
