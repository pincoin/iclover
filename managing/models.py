import re

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from member.models import *
from datetime import datetime, timedelta

# Create your models here.

class Product(TimeStampedModel):
    purchase = models.ForeignKey(
        'member.Profile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    state = models.IntegerField(
        verbose_name=_('state'),
        blank=True,
        null=True,
    )

    name = models.CharField(
        verbose_name=_('name of product'),
        max_length=255,
        blank=True,
    )

    standard = models.CharField(
        verbose_name=_('standard'),
        max_length=255,
        blank=True,
    )

    purchase_price = models.FloatField(
        verbose_name=_('purchase_price'),
        blank=True,
    )

    sale_price = models.FloatField(
        verbose_name=_('sale_price'),
        blank=True,
    )

    delivery_charge = models.IntegerField(
        verbose_name=_('delivery charge'),
        blank=True,
    )

    quantity = models.IntegerField(
        verbose_name=_('min quantity'),
        blank=True,
    )

    group = models.CharField(
        verbose_name=_('group of product'),
        max_length=255,
        blank=True,
    )

    manage_code = models.CharField(
        verbose_name=_('manage_code'),
        max_length=255,
        blank=True,
    )



    def upload_to_product(instance, filename):
        return 'product/{}/{}'.format(instance.purchase, filename)
    product_img = models.ImageField(
        verbose_name=_('product_img'),
        blank= True,
        upload_to= upload_to_product,
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return '{} {} {}'.format(self.purchase, self.name, self.state)

class Sample(TimeStampedModel):
    employees = models.ForeignKey(
        'member.Employees',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    plush_date = models.DateTimeField(
        verbose_name=_('plush_date'),
        auto_now_add=True,
    )

    finish_date = models.DateTimeField(
        verbose_name=_('finish_date'),
        default=datetime.now() + timedelta(days=90),
    )

    name = models.CharField(
        verbose_name=_('name of sample'),
        max_length=255,
        blank=True,
    )

    keyword = models.CharField(
        verbose_name=_('keyword'),
        max_length=255,
        blank=True,
    )

    group = models.CharField(
        verbose_name=_('group of sample'),
        max_length=255,
        blank=True,
    )

    def upload_to_sample(instance, filename):
        now = datetime.now()
        nowDate = now.strftime('%Y')
        return 'sample/{}/{}/{}'.format(instance.employees,nowDate, filename)
    sample_img = models.ImageField(
        verbose_name=_('sample_img'),
        blank=True,
        upload_to=upload_to_sample,
    )

    class Meta:
        verbose_name = _('sample')
        verbose_name_plural = _('samples')

    def __str__(self):
        return '{} {} {}'.format(self.name, self.employees, self.keyword)
