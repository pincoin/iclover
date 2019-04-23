import re

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import SoftDeletableModel, TimeStampedModel
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
        max_digits=11,
    )

    sale_price = models.DecimalField(
        verbose_name=_('sale_price'),
        blank=True,
        decimal_places=4,
        max_digits=11,
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

class Deposit(TimeStampedModel, SoftDeletableModel):
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

class Employees(TimeStampedModel, SoftDeletableModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    state = models.IntegerField(
        verbose_name=_('state'),
        blank=True,
        null=True,
    )

    name = models.CharField(
        verbose_name=_('name of employees'),
        max_length=255,
        blank=True,
        null=True,
    )

    join = models.DateField(
        verbose_name=_('Join'),
        blank=True,
        null=True,
    )

    leave = models.DateField(
        verbose_name=_('leave'),
        blank=True,
        null=True,
    )

    cellphone = models.CharField(
        verbose_name=_('cellphone'),
        max_length=255,
        blank=True,
        null=True,
    )

    def upload_to_employees(instance, filename):
        return 'employees/{}/{}'.format(instance.user.name, filename)
    join_pic = models.ImageField(
        verbose_name=_('join picture'),
        null=True,
        blank= True,
        upload_to= upload_to_employees,
    )
    leave_pic = models.ImageField(
        verbose_name=_('leave picture'),
        null=True,
        blank=True,
        upload_to=upload_to_employees,
    )

    class Meta:
        verbose_name = _('직원')
        verbose_name_plural = _('직원')

    def __str__(self):
        return '{} {} {}'.format(self.user, self.name, self.state)

class Ask(TimeStampedModel, SoftDeletableModel):
    ASK_PART_WHAT_TO_DO = Choices(
        (0, '환불', _('환불')),
        (1, '입금', _('입금')),
        (2, '영수증/계산서', _('영수증/계산서')),
    )

    ask_from = models.CharField(
        verbose_name=_('name of employees requester'),
        max_length=255,
        blank=True,
    )

    ask_to = models.ForeignKey(
        'Employees',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    ask_part = models.IntegerField(
        verbose_name=_('division of requests'),
        choices=ASK_PART_WHAT_TO_DO,
        blank=True,
        db_index=True,
    )

    ask_what = models.CharField(
        verbose_name=_('request comment'),
        max_length=255,
        blank=True,
    )

    ask_finish = models.BooleanField(
        verbose_name=_('ask_finish'),
        blank=True,
        default=False,
    )

    class Meta:
        verbose_name = _('요청사항')
        verbose_name_plural = _('요청사항')

    def __str__(self):
        return '{} to {} state:{} {}'.format(self.ask_from, self.ask_to, self.ask_part, self.ask_what)

class Sample(TimeStampedModel, SoftDeletableModel):
    category = models.ForeignKey(
        'design.Category',
        blank=True,
        null=True,
        verbose_name=_('카테고리'),
        db_index=True,
        on_delete=models.SET_NULL,
    )
    sectors_category = models.ForeignKey(
        'design.SectorsCategory',
        blank=True,
        null=True,
        verbose_name=_('업종'),
        db_index=True,
        on_delete=models.SET_NULL,
    )

    employees = models.ForeignKey(
        'Employees',
        on_delete=models.SET_NULL,
        verbose_name=_('직원명'),
        null=True,
        blank=True,
    )

    plush_date = models.DateTimeField(
        verbose_name=_('등록일'),
        auto_now_add=True,
    )

    name = models.CharField(
        verbose_name=_('샘플명'),
        max_length=255,
        blank=True,
    )

    keyword = models.CharField(
        verbose_name=_('키워드'),
        max_length=255,
        blank=True,
    )

    group = models.CharField(
        verbose_name=_('샘플 패키지'),
        max_length=255,
        blank=True,
    )

    def upload_to_sample(instance, filename):
        now = datetime.now()
        nowDate = now.strftime('%Y')
        return 'sample/{}/{}/{}'.format(instance.category,nowDate, filename)
    sample_img = models.ImageField(
        verbose_name=_('sample_img'),
        blank=True,
        upload_to=upload_to_sample,
    )

    class Meta:
        verbose_name = _('샘플')
        verbose_name_plural = _('샘플')

    def __str__(self):
        return '{} {} {}'.format(self.name, self.employees, self.keyword)

