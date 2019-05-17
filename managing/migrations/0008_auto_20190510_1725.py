# Generated by Django 2.1.7 on 2019-05-10 08:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0004_auto_20190423_0045'),
        ('managing', '0007_auto_20190429_2334'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('employees', models.CharField(blank=True, max_length=255, null=True, verbose_name='담당자')),
                ('content', models.CharField(blank=True, max_length=255, null=True, verbose_name='내용')),
                ('confirm', models.BooleanField(default=False, verbose_name='확인')),
                ('common', models.BooleanField(default=False, verbose_name='개인/공유')),
                ('importance', models.BooleanField(default=False, verbose_name='중요도')),
                ('notice', models.BooleanField(default=False, verbose_name='공지사항')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='design.OrderInfo', verbose_name='품목 연결')),
            ],
            options={
                'verbose_name': '할일 to_do',
                'verbose_name_plural': '할일 to_do',
            },
        ),
        migrations.AlterField(
            model_name='ask',
            name='ask_part',
            field=models.IntegerField(choices=[(0, '환불'), (1, '입금 요청'), (2, '영수증/계산서'), (3, '기타')], db_index=True, verbose_name='division of requests'),
        ),
    ]
