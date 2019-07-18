# Generated by Django 2.1.7 on 2019-06-27 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0022_auto_20190626_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlist',
            name='order_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_list', to='design.OrderInfo', verbose_name='주문 정보'),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, null=True, verbose_name='매입가'),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='price_tax',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, null=True, verbose_name='매입 부가세'),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='selling_price',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, null=True, verbose_name='판매가'),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='selling_price_tax',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, null=True, verbose_name='판매 부가세'),
        ),
    ]