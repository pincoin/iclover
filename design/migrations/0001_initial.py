# Generated by Django 2.1.7 on 2019-03-27 09:25

import design.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusuOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='slug')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'verbose_name': '옵션 수량',
                'verbose_name_plural': '옵션 수량',
            },
        ),
        migrations.CreateModel(
            name='BusuOptionValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('value', models.IntegerField(db_index=True, default=0, verbose_name='value')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
            ],
            options={
                'verbose_name': '옵션 수량 값',
                'verbose_name_plural': '옵션 수량 value',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='slug')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='design.Category', verbose_name='parent')),
            ],
            options={
                'verbose_name': '품목 카테고리',
                'verbose_name_plural': '품목 카테고리 정리',
            },
        ),
        migrations.CreateModel(
            name='DosuOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='slug')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DosuOption', to='design.Category', verbose_name='category')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='design.DosuOption', verbose_name='parent')),
            ],
            options={
                'verbose_name': '옵션 도수',
                'verbose_name_plural': '옵션 도수',
            },
        ),
        migrations.CreateModel(
            name='DosuOptionValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('value', models.IntegerField(db_index=True, default=0, verbose_name='value')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
            ],
            options={
                'verbose_name': '옵션 도수 값',
                'verbose_name_plural': '옵션 도수 value',
            },
        ),
        migrations.CreateModel(
            name='Goods_banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('category', models.IntegerField(blank=True, choices=[(0, '전단지/포스터'), (1, '문어발'), (2, '명함'), (3, '복권'), (4, '상품권'), (5, '스티커'), (6, '종이자석'), (7, '양식지/NCR지'), (8, '카달로그/브로셔'), (9, '포스트잇'), (10, '떡메모지'), (21, '현수막'), (22, '게시대현수막'), (23, '족자'), (24, '실사출력'), (31, '배너'), (32, '대형배너'), (33, '미니배너'), (33, '가방배너'), (34, '배너부속품'), (41, '명찰/사원증'), (42, '부채'), (43, '물티슈'), (44, '에어탑'), (45, '어깨띠'), (51, '운동복'), (52, '수건'), (53, '샤워용품'), (54, '청소용품'), (55, '평상/원목'), (99, '메인배너')], db_index=True, verbose_name='category')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
                ('subtitle', models.CharField(blank=True, max_length=255, verbose_name='subtitle')),
                ('state', models.IntegerField(blank=True, default=0, verbose_name='state of banner')),
                ('goods_banner_img', models.ImageField(blank=True, upload_to=design.models.Goods_banner.upload_to_banner, verbose_name='product banner img for introduction')),
            ],
            options={
                'verbose_name': '상품 배너',
                'verbose_name_plural': '상품별 배너',
            },
        ),
        migrations.CreateModel(
            name='NamecardOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='slug')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='design.Category', verbose_name='category')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='design.Option', verbose_name='parent')),
            ],
            options={
                'verbose_name': '옵션 기타',
                'verbose_name_plural': '옵션 기타',
            },
        ),
        migrations.CreateModel(
            name='OptionValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('value', models.IntegerField(db_index=True, default=0, verbose_name='value')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
                ('option', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='option_values', to='design.Option', verbose_name='option')),
            ],
            options={
                'verbose_name': '옵션 기타 값',
                'verbose_name_plural': '옵션 기타 value',
            },
        ),
        migrations.CreateModel(
            name='PaperOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='slug')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PaperOption', to='design.Category', verbose_name='category')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='design.PaperOption', verbose_name='parent')),
            ],
            options={
                'verbose_name': '옵션 용지',
                'verbose_name_plural': '옵션 용지',
            },
        ),
        migrations.CreateModel(
            name='PaperOptionValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('value', models.IntegerField(db_index=True, default=0, verbose_name='value')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
            ],
            options={
                'verbose_name': '옵션 용지 값',
                'verbose_name_plural': '옵션 용지 value',
            },
        ),
        migrations.CreateModel(
            name='SectorsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='slug')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='design.SectorsCategory', verbose_name='parent')),
            ],
            options={
                'verbose_name': '업종 카테고리',
                'verbose_name_plural': '업종 카테고리 정리',
            },
        ),
        migrations.CreateModel(
            name='StandardOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='slug')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='StandardOption', to='design.Category', verbose_name='category')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='design.StandardOption', verbose_name='parent')),
            ],
            options={
                'verbose_name': '옵션 규격',
                'verbose_name_plural': '옵션 규격',
            },
        ),
        migrations.CreateModel(
            name='StandardOptionValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('value', models.IntegerField(db_index=True, default=0, verbose_name='value')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
                ('option', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='standard_option_values', to='design.StandardOption', verbose_name='option')),
            ],
            options={
                'verbose_name': '옵션 규격 값',
                'verbose_name_plural': '옵션 규격 value',
            },
        ),
        migrations.AddField(
            model_name='paperoptionvalue',
            name='option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paper_option_values', to='design.StandardOption', verbose_name='option'),
        ),
        migrations.AddField(
            model_name='dosuoptionvalue',
            name='option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dosu_option_values', to='design.StandardOption', verbose_name='option'),
        ),
        migrations.AddField(
            model_name='busuoptionvalue',
            name='option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='busu_option_values', to='design.StandardOption', verbose_name='option'),
        ),
        migrations.AddField(
            model_name='busuoption',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BusuOption', to='design.Category', verbose_name='category'),
        ),
        migrations.AddField(
            model_name='busuoption',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='design.BusuOption', verbose_name='parent'),
        ),
    ]
