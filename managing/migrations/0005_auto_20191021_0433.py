# Generated by Django 2.1.7 on 2019-10-20 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0004_auto_20191004_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderwithdeposit',
            name='order_info_with',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_info_with', to='design.CustomerOrderInfo'),
        ),
    ]
