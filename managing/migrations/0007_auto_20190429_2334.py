# Generated by Django 2.1.7 on 2019-04-29 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0006_auto_20190429_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='bank',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='은행명'),
        ),
        migrations.AddField(
            model_name='deposit',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='날짜'),
        ),
        migrations.AddField(
            model_name='deposit',
            name='part',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='입/출금'),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='amount',
            field=models.IntegerField(blank=True, verbose_name='입금액'),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='bill',
            field=models.CharField(blank=True, max_length=255, verbose_name='영수처리'),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='memo',
            field=models.CharField(blank=True, max_length=255, verbose_name='메모'),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='입금자명'),
        ),
    ]