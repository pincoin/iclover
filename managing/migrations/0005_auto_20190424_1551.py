# Generated by Django 2.1.7 on 2019-04-24 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0004_sample_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ask',
            name='ask_from',
            field=models.CharField(blank=True, max_length=255, verbose_name='질문자'),
        ),
        migrations.AlterField(
            model_name='ask',
            name='ask_part',
            field=models.IntegerField(blank=True, choices=[(0, '환불'), (1, '입금 요청'), (2, '영수증/계산서'), (3, '기타')], db_index=True, verbose_name='division of requests'),
        ),
        migrations.AlterField(
            model_name='ask',
            name='ask_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='managing.Employees', verbose_name='받는사람'),
        ),
        migrations.AlterField(
            model_name='ask',
            name='ask_what',
            field=models.CharField(blank=True, max_length=255, verbose_name='요청내용'),
        ),
    ]