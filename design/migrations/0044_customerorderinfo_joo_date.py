# Generated by Django 2.1.7 on 2019-10-16 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0043_customerorderproduct_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorderinfo',
            name='joo_date',
            field=models.DateField(blank=True, null=True, verbose_name='주문일'),
        ),
    ]
