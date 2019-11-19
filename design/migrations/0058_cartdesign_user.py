# Generated by Django 2.1.7 on 2019-11-14 04:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('design', '0057_cartdesign_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartdesign',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='고객'),
        ),
    ]
