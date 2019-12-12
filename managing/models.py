import re

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import Thumbnail, ResizeToFit
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import SoftDeletableModel, TimeStampedModel
from datetime import datetime, timedelta

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
        return f'product/{instance.purchase}/{filename}'
    product_img = models.ImageField(
        verbose_name=_('product_img'),
        blank= True,
        upload_to= upload_to_product,
    )

    class Meta:
        verbose_name = _('품목')
        verbose_name_plural = _('품목')

    def __str__(self):
        return f'{self.purchase} {self.name} {self.state}'

class Deposit(TimeStampedModel, SoftDeletableModel):
    date = models.DateTimeField(
        verbose_name=_('날짜'),
        blank = True,
        null = True,
    )

    bank = models.CharField(
        verbose_name=_('은행명'),
        max_length=100,
        blank=True,
        null=True,
    )

    part = models.CharField(
        verbose_name=_('입/출금'),
        max_length= 100,
        blank=True,
        null=True,

    )

    name = models.CharField(
        verbose_name=_('입금자명'),
        max_length=255,
        blank=True,
    )

    amount = models.IntegerField(
        verbose_name=_('입금액'),
        blank=True,
    )

    memo = models.CharField(
        verbose_name=_('메모'),
        max_length=255,
        blank=True,
    )

    bill = models.CharField(
        verbose_name=_('영수처리'),
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
        return f'{self.name} {self.amount} {self.memo}'

class OrderWithDeposit(TimeStampedModel):
    order_info_with = models.ForeignKey(
        'design.CustomerOrderInfo',
        on_delete=models.SET_NULL,
        related_name='order_info_with',
        null=True,
        blank=True,
    )
    deposit_with = models.ForeignKey(
        'managing.Deposit',
        on_delete=models.SET_NULL,
        related_name='deposit_with',
        null=True,
        blank=True,
    )
    division =models.IntegerField(
        verbose_name='수동 확인',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('입금 연결')
        verbose_name_plural = _('입금 연결')

    def __str__(self):
        return f'{self.order_info_with} {self.deposit_with}'

class SpecialPrice(TimeStampedModel):
    product = models.ForeignKey(
        'design.ProductText',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    new_price = models.DecimalField(
        verbose_name=_('new_price'),
        decimal_places=4,
        max_digits=11,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('특별가격')
        verbose_name_plural = _('특별가격')

    def __str__(self):
        return f'{self.product} {self.customer} {self.new_price}'

class Discount(TimeStampedModel):
    product = models.ForeignKey(
        'design.ProductText',
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
        return f'{self.product} {self.discount1} {self.discount2} {self.discount3}'

class Employees(TimeStampedModel, SoftDeletableModel):
    GROUP_EM = Choices(
        (0, '관리자', _('관리자')),
        (1, '팀장', _('팀장')),
        (2, '디자이너', _('디자이너')),
        (3, '알바', _('알바')),
        (4, '기타', _('기타')),
    )

    group = models.IntegerField(
        verbose_name=_('그룹선택'),
        default=2,
        choices=GROUP_EM,
        db_index=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    state = models.BooleanField(
        verbose_name=_('state'),
        default=True,
    )

    name = models.CharField(
        verbose_name=_('name of employees'),
        max_length=255,
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
        return 'employees/{}/{}'.format(instance.name, filename)
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
        return '{}'.format(self.user)

class Ask(TimeStampedModel, SoftDeletableModel):
    ASK_PART_WHAT_TO_DO = Choices(
        (0, '환불', _('환불')),
        (1, '입금 요청', _('입금 요청')),
        (2, '영수증/계산서', _('영수증/계산서')),
        (3, '기타', _('기타')),
    )

    ask_from = models.CharField(
        verbose_name=_('질문자'),
        max_length=255,
        blank=True,
    )

    ask_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('받는사람'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    ask_part = models.IntegerField(
        verbose_name=_('division of requests'),
        choices=ASK_PART_WHAT_TO_DO,
        db_index=True,
    )

    ask_what = models.CharField(
        verbose_name=_('요청내용'),
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
        return f'{self.ask_from} to {self.ask_to} state:{self.ask_part} {self.ask_what}'

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
        settings.AUTH_USER_MODEL,
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
    state = models.BooleanField(
        verbose_name=_('샘플 상태'),
        default=True,
    )
    link = models.CharField(
        verbose_name=_('링크 url'),
        max_length=255,
        blank=True,
    )

    ASPECT_CHO = Choices(
        (0, '가로', _('가로')),
        (1, '세로', _('세로')),
    )
    aspect = models.IntegerField(
        verbose_name=_('가로 / 세로'),
        default=0,
        choices=ASPECT_CHO,
    )

    def upload_to_sample(instance, filename):
        now = datetime.now()
        nowDate = now.strftime('%Y')
        return f'sample/{instance.category}/{nowDate}/{filename}'

    images = ProcessedImageField(
        verbose_name=_('sample_img'),
        processors=[ResizeToFit(600, 600)],
        blank=True,
        upload_to=upload_to_sample,
    )

    def save(self, request=False, *args, **kwargs):
        super(Sample, self).save(*args, **kwargs)

    def image_tag(self):
        return mark_safe(f'<img src="{self.images.url}" style="max-height: 200px; max-width: 200px;"/>')

    image_tag.short_description = 'Image'

    class Meta:
        verbose_name = _('샘플')
        verbose_name_plural = _('샘플')

    def __str__(self):
        return f'{self.name} {self.employees} {self.keyword}'

class Memo(TimeStampedModel, SoftDeletableModel):
    order = models.ForeignKey(
        'design.OrderInfo',
        blank=True,
        null=True,
        verbose_name=_('품목 연결'),
        db_index=True,
        on_delete=models.SET_NULL,
    )

    employees = models.CharField(
        verbose_name=_('담당자'),
        max_length=255,
        blank=True,
        null=True,
    )

    content = models.CharField(
        verbose_name=_('내용'),
        max_length=255,
        blank=True,
        null=True,
    )

    confirm = models.BooleanField(
        default=False,
        verbose_name=_('확인'),
    )

    common = models.BooleanField(
        default=False,
        verbose_name=_('개인/공유'),
    )

    importance = models.BooleanField(
        default=False,
        verbose_name=_('중요도'),
    )

    notice = models.BooleanField(
        default=False,
        verbose_name=_('공지사항'),
    )

    class Meta:
        verbose_name = _('할일 to_do')
        verbose_name_plural = _('할일 to_do')



class CustomerMemo(TimeStampedModel):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name= 'customer_memo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    keyword = models.CharField(
        verbose_name=_('키워드'),
        max_length=255,
        blank=True,
        null=True,
    )

    manager = models.CharField(
        verbose_name=_('담당자'),
        max_length=255,
        blank=True,
        null=True,
    )

    memo = models.CharField(
        verbose_name=_('메모'),
        max_length=255,
        blank=True,
        null=True,
    )

    confirm = models.CharField(
        verbose_name=_('시안 확인'),
        max_length=255,
        blank=True,
        null=True,
    )

    hoo = models.CharField(
        verbose_name=_('후가공'),
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.customer}"

    class Meta:
        verbose_name = _('고객 프로필 추가정보 using inside')
        verbose_name_plural = _('고객 프로필 추가정보 using inside')
