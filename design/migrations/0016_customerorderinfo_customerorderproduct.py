# Generated by Django 2.1.7 on 2019-09-30 06:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('design', '0015_auto_20190927_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerOrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='회사명')),
                ('uuid', models.CharField(blank=True, max_length=255, null=True, verbose_name='uuid')),
                ('code', models.IntegerField(blank=True, null=True, verbose_name='사업자번호')),
                ('phone', models.CharField(blank=True, max_length=255, verbose_name='폰 번호')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='주소')),
                ('address2', models.CharField(blank=True, max_length=255, verbose_name='주소2')),
                ('address_detail', models.CharField(blank=True, max_length=255, verbose_name='상세주소')),
                ('address_option', models.CharField(blank=True, max_length=255, verbose_name='주소 참고')),
                ('bill_select', models.IntegerField(blank=True, choices=[(0, '세금계산서'), (1, '사업자 지출증빙'), (2, '현금 영수증'), (3, '미발행')], null=True, verbose_name='사업자 상태')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='고객')),
            ],
            options={
                'verbose_name': '고객 주문 기본 정보',
                'verbose_name_plural': '고객 주문 기본 정보',
            },
        ),
        migrations.CreateModel(
            name='CustomerOrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='규격 size')),
                ('size_value', models.CharField(blank=True, max_length=255, null=True, verbose_name='규격 size value')),
                ('paper', models.CharField(blank=True, max_length=255, null=True, verbose_name='용지 paper')),
                ('paper_value', models.CharField(blank=True, max_length=255, null=True, verbose_name='용지 paper value')),
                ('side', models.CharField(blank=True, max_length=255, null=True, verbose_name='인쇄 side')),
                ('side_value', models.CharField(blank=True, max_length=255, null=True, verbose_name='인쇄 side value')),
                ('deal', models.CharField(blank=True, max_length=255, null=True, verbose_name='수량 deal')),
                ('deal_value', models.CharField(blank=True, max_length=255, null=True, verbose_name='수량 deal value')),
                ('option1', models.CharField(blank=True, max_length=255, null=True, verbose_name='옵션1 option1')),
                ('option1_value', models.CharField(blank=True, max_length=255, null=True, verbose_name='옵션1 option1 value')),
                ('option2', models.CharField(blank=True, max_length=255, null=True, verbose_name='옵션1 option2')),
                ('option2_value', models.CharField(blank=True, max_length=255, null=True, verbose_name='옵션1 option2 value')),
                ('supplier', models.CharField(blank=True, max_length=255, null=True, verbose_name='매입')),
                ('sell', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, verbose_name='sell')),
                ('sell_opposition', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=11, verbose_name='buy')),
                ('sectors_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='design.CustomerOrderInfo', verbose_name='고객 주문 정보')),
            ],
            options={
                'verbose_name': '고객 주문 품목',
                'verbose_name_plural': '고객 주문 품목',
            },
        ),
    ]
