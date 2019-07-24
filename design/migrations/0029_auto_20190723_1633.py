# Generated by Django 2.1.7 on 2019-07-23 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0028_orderimg_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='orderimg',
            name='order_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_img', to='design.OrderInfo', verbose_name='주문 리스트'),
        ),
        migrations.AlterField(
            model_name='producttext',
            name='buy_price',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, null=True, verbose_name='매입가'),
        ),
        migrations.AlterField(
            model_name='producttext',
            name='height',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, null=True, verbose_name='높이'),
        ),
        migrations.AlterField(
            model_name='producttext',
            name='horizontal',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, null=True, verbose_name='가로'),
        ),
        migrations.AlterField(
            model_name='producttext',
            name='quantity',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, null=True, verbose_name='메인 수량'),
        ),
        migrations.AlterField(
            model_name='producttext',
            name='sell_price',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, null=True, verbose_name='판매가'),
        ),
        migrations.AlterField(
            model_name='producttext',
            name='vertical',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, null=True, verbose_name='세로'),
        ),
        migrations.AlterField(
            model_name='producttext',
            name='width',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, null=True, verbose_name='넓이'),
        ),
    ]
