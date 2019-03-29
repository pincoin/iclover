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

    purchase_price = models.DecimalField(
        verbose_name=_('purchase_price'),
        blank=True,
        decimal_places=4,
        max_digits=100,
    )

    sale_price = models.DecimalField(
        verbose_name=_('sale_price'),
        blank=True,
        decimal_places=4,
        max_digits=100,
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
        verbose_name = _('품목')
        verbose_name_plural = _('품목')

    def __str__(self):
        return '{} {} {}'.format(self.purchase, self.name, self.state)

class Deposit(TimeStampedModel):
    name = models.CharField(
        verbose_name=_('name of the deposit'),
        max_length=255,
        blank=True,
    )

    amount = models.IntegerField(
        verbose_name=_('amount'),
        blank=True,
    )

    memo = models.CharField(
        verbose_name=_('memo and company name of deposit'),
        max_length=255,
        blank=True,
    )

    bill = models.CharField(
        verbose_name=_('bill sate of deposit'),
        max_length=255,
        blank=True,
    )
    state = models.BooleanField(
        verbose_name=_('sate of deposit'),
        blank=True,
        default=False,
    )

    class Meta:
        verbose_name = _('입금내역')
        verbose_name_plural = _('입금내역')

    def __str__(self):
        return '{} {} {}'.format(self.name, self.amount, self.memo)

class Discount(TimeStampedModel):
    product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    discount1 = models.IntegerField(
        verbose_name=_('discount1'),
        blank=True,
    )

    discount2 = models.IntegerField(
        verbose_name=_('discount2'),
        blank=True,
    )

    discount3 = models.IntegerField(
        verbose_name=_('discount3'),
        blank=True,
    )

    class Meta:
        verbose_name = _('할인율')
        verbose_name_plural = _('할인율')

    def __str__(self):
        return '{} {} {} {}'.format(self.product, self.discount1, self.discount2, self.discount3)