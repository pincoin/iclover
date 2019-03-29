import re
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import (
    SoftDeletableModel, TimeStampedModel
)
from member.models import *
from datetime import datetime, timedelta
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel



class Goods_banner(TimeStampedModel):
    CATEGORY_GOODS_BANNER = Choices(
        (0, '전단지/포스터', _('전단지/포스터')),
        (1, '문어발', _('문어발')),
        (2, '명함', _('명함')),
        (3, '복권', _('복권')),
        (4, '상품권', _('상품권')),
        (5, '스티커', _('스티커')),
        (6, '종이자석', _('종이자석')),
        (7, '양식지/NCR지', _('양식지/NCR지')),
        (8, '카달로그/브로셔', _('카달로그/브로셔')),
        (9, '포스트잇', _('포스트잇')),
        (10, '떡메모지', _('떡메모지')),
        (21, '현수막', _('현수막')),
        (22, '게시대현수막', _('게시대현수막')),
        (23, '족자', _('족자')),
        (24, '실사출력', _('실사출력')),
        (31, '배너', _('배너')),
        (32, '대형배너', _('대형배너')),
        (33, '미니배너', _('미니배너')),
        (33, '가방배너', _('가방배너')),
        (34, '배너부속품', _('배너부속품')),
        (41, '명찰/사원증', _('명찰/사원증')),
        (42, '부채', _('부채')),
        (43, '물티슈', _('물티슈')),
        (44, '에어탑', _('에어탑')),
        (45, '어깨띠', _('어깨띠')),
        (51, '운동복', _('운동복')),
        (52, '수건', _('수건')),
        (53, '샤워용품', _('샤워용품')),
        (54, '청소용품', _('청소용품')),
        (55, '평상/원목', _('평상/원목')),
        (99, '메인배너', _('메인배너')),
    )

    category = models.IntegerField(
        verbose_name=_('category'),
        choices=CATEGORY_GOODS_BANNER,
        blank=True,
        db_index=True,
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        blank=True,
    )

    subtitle = models.CharField(
        verbose_name=_('subtitle'),
        max_length=255,
        blank=True,
    )

    state = models.IntegerField(
        verbose_name=_('state of banner'),
        blank=True,
        default=0,
    )

    def upload_to_banner(instance, filename):
        now = datetime.now()
        nowDate = now.strftime('%Y')
        return 'goods_banner/{}/{}/{}'.format(instance.category, nowDate, filename)

    goods_banner_img = models.ImageField(
        verbose_name=_('product banner img for introduction'),
        blank=True,
        upload_to=upload_to_banner,
    )

    class Meta:
        verbose_name = _('노출 배너')
        verbose_name_plural = _('노출 배너')

    def __str__(self):
        return '{} / {}'.format(self.get_category_display(), self.subtitle)


class Category(TimeStampedModel, MPTTModel):
    parent = TreeForeignKey(
        'self',
        verbose_name=_('parent'),
        blank=True,
        null=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=128,
    )

    slug = models.SlugField(
        verbose_name=_('slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        verbose_name = _('카테고리 품목')
        verbose_name_plural = _('카테고리 품목')

    def __str__(self):
        return self.title

class SectorsCategory(TimeStampedModel, MPTTModel):
    parent = TreeForeignKey(
        'self',
        verbose_name=_('parent'),
        blank=True,
        null=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=128,
    )

    slug = models.SlugField(
        verbose_name=_('slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        verbose_name = _('카테고리 업종')
        verbose_name_plural = _('카테고리 업종')

    def __str__(self):
        return self.title

class Option(TimeStampedModel, MPTTModel):
    category = models.ForeignKey(
        'design.Category',
        verbose_name=_('category'),
        related_name='options',
        null=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    parent = TreeForeignKey(
        'self',
        verbose_name=_('parent'),
        blank=True,
        null=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=128,
    )

    slug = models.SlugField(
        verbose_name=_('slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        verbose_name = _('상품옵션 기타')
        verbose_name_plural = _('상품옵션 기타')

    def __str__(self):
        return self.title

class StandardOption(TimeStampedModel, MPTTModel):
    category = models.ForeignKey(
        'design.Category',
        verbose_name=_('category'),
        related_name='StandardOption',
        null=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    parent = TreeForeignKey(
        'self',
        verbose_name=_('parent'),
        blank=True,
        null=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=128,
    )

    slug = models.SlugField(
        verbose_name=_('slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )
    horizontal = models.DecimalField(
        verbose_name=_('가로'),
        max_digits=100,
        decimal_places=4,
        null=True,
        blank=True,
    )
    vertical = models.DecimalField(
        verbose_name=_('세로'),
        max_digits=100,
        decimal_places=4,
        null=True,
        blank=True,
    )
    width = models.DecimalField(
        verbose_name=_('넓이'),
        max_digits=100,
        decimal_places=4,
        null=True,
        blank=True,
    )
    height = models.DecimalField(
        verbose_name=_('높이'),
        max_digits=100,
        decimal_places=4,
        null=True,
        blank=True,
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        verbose_name = _('상품옵션 규격')
        verbose_name_plural = _('상품옵션 규격')

    def __str__(self):
        return self.title

class PaperOption(TimeStampedModel, MPTTModel):
    category = models.ForeignKey(
        'design.Category',
        verbose_name=_('category'),
        related_name='PaperOption',
        null=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    parent = TreeForeignKey(
        'self',
        verbose_name=_('parent'),
        blank=True,
        null=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=128,
    )

    slug = models.SlugField(
        verbose_name=_('slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )
    gram = models.IntegerField(
        verbose_name=_('그람수'),
        blank=True,
        null=True,
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        verbose_name = _('상품옵션 용지')
        verbose_name_plural = _('상품옵션 용지')

    def __str__(self):
        return self.title

class DosuOption(TimeStampedModel, MPTTModel):
    category = models.ForeignKey(
        'design.Category',
        verbose_name=_('category'),
        related_name='DosuOption',
        null=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    parent = TreeForeignKey(
        'self',
        verbose_name=_('parent'),
        blank=True,
        null=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=128,
    )

    slug = models.SlugField(
        verbose_name=_('slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        verbose_name = _('상품옵션 도수')
        verbose_name_plural = _('상품옵션 도수')

    def __str__(self):
        return self.title

class BusuOption(TimeStampedModel, MPTTModel):
    category = models.ForeignKey(
        'design.Category',
        verbose_name=_('category'),
        related_name='BusuOption',
        null=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    parent = TreeForeignKey(
        'self',
        verbose_name=_('parent'),
        blank=True,
        null=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=128,
    )

    slug = models.SlugField(
        verbose_name=_('slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        allow_unicode=True,
    )

    quantity = models.IntegerField(
        verbose_name=_('수량'),
        null=True,
        blank=True,
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        verbose_name = _('상품옵션 수량')
        verbose_name_plural = _('상품옵션 수량')

    def __str__(self):
        return self.title


class ProductPrice(TimeStampedModel):
    code = models.IntegerField(
        null=True,
        blank=True,
    )
    option = models.ForeignKey(
        'design.Option',
        verbose_name=_('기타 옵션'),
        null=True,
        blank= True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    standard_option = models.ForeignKey(
        'design.StandardOption',
        verbose_name=_('기본 옵션'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )
    paper_option = models.ForeignKey(
        'design.PaperOption',
        verbose_name=_('용지 옵션'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )
    dosu_option = models.ForeignKey(
        'design.DosuOption',
        verbose_name=_('도수 옵션'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )
    busu_option = models.ForeignKey(
        'design.BusuOption',
        verbose_name=_('수량 옵션'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )
    purchase = models.ForeignKey(
        'member.Profile',
        verbose_name=_('매입처'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    price = models.DecimalField(
        max_digits=100,
        decimal_places=4,
        null=True,
        blank=True,
    )
    selling_price = models.DecimalField(
        max_digits=100,
        decimal_places=4,
        null=True,
        blank=True,
    )
    group_product = models.CharField(
        verbose_name=_('품목 그룹'),
        max_length=100,
        null=True,
        blank=True,
    )
    group_manage = models.CharField(
        verbose_name=_('관리 항목'),
        max_length=100,
        null=True,
        blank=True,
    )
    info = models.CharField(
        verbose_name=_('품목 정보'),
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('상품옵션 최종 가격')
        verbose_name_plural = _('상품옵션 최종 가격')

    def __str__(self):
        return '{} {} {}'.format(self.standard_option,self.price,self.selling_price)

class OrderInfo(TimeStampedModel):
    profile = models.ForeignKey(
        'member.Profile',
        verbose_name=_('거래처'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )
    employees = models.ForeignKey(
        'member.Employees',
        verbose_name=_('작업자'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    company = models.CharField(
        verbose_name=_('업체명'),
        max_length=100,
        null=True,
        blank=True,
    )

    address = models.CharField(
        verbose_name=_('주소'),
        max_length=100,
        null=True,
        blank=True,
    )
    tel = models.CharField(
        verbose_name=_('연락처'),
        max_length=100,
        null=True,
        blank=True,
    )

    STATE_WHAT = Choices(
        (0, '견적', _('견적')),
        (1, '주문', _('주문')),
        (2, '완료', _('완료')),
        (3, '입금대기', _('입금대기')),
        (4, '취소', _('취소')),
        (5, '보류', _('보류')),
        (6, '환불', _('환불')),
    )

    state = models.IntegerField(
        verbose_name=_('상태값'),
        choices=STATE_WHAT,
        default= 0,
        blank=True,
        db_index=True,
    )
    order_date = models.CharField(
        verbose_name=_('발주일'),
        max_length=100,
        null=True,
        blank=True,
    )
    keywords = models.CharField(
        verbose_name=_('검색창 내용'),
        max_length=1000,
        null=True,
        blank=True,
    )
    checker = models.CharField(
        verbose_name=_('시안 확인'),
        max_length=100,
        null=True,
        blank=True,
    )
    deposit = models.CharField(
        verbose_name=_('입금 확인'),
        max_length=100,
        null=True,
        blank=True,
    )
    options = models.CharField(
        verbose_name=_('결제/포함/택배'),
        max_length=100,
        null=True,
        blank=True,
    )


    uuid = models.UUIDField(
        default=uuid.uuid1
    )

    class Meta:
        verbose_name = _('주문 1_정보')
        verbose_name_plural = _('주문 1_정보')

    def __str__(self):
        return '{} {} {}'.format(self.profile, self.company, self.employees)

class OrderList(TimeStampedModel):
    order_info = models.ForeignKey(
        'design.OrderInfo',
        verbose_name=_('주문 정보'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )
    # 정렬할 경우 품목의 리스트 순서를 정하는 번호
    list_sort = models.IntegerField(
        verbose_name=_('내역 순서'),
        db_index=True,
    )
    code = models.IntegerField(
        verbose_name=_('품목코드'),
        db_index=True,
    )
    name = models.CharField(
        verbose_name=_('제품명'),
        max_length=100,
        null=True,
        blank=True,
    )
    standard = models.CharField(
        verbose_name=_('규격'),
        max_length=100,
        null=True,
        blank=True,
    )
    quantity = models.IntegerField(
        verbose_name=_('수량'),
        db_index=True,
    )
    price = models.DecimalField(
        verbose_name=_('매입가'),
        max_digits=100,
        decimal_places=4,
        null=True,
        blank=True,
    )
    price_tax = models.DecimalField(
        verbose_name=_('매입 부가세'),
        max_digits=100,
        decimal_places=4,
        null=True,
        blank=True,
    )
    selling_price = models.DecimalField(
        verbose_name=_('판매가'),
        max_digits=100,
        decimal_places=4,
        null=True,
        blank=True,
    )
    selling_price_tax = models.DecimalField(
        verbose_name=_('판매 부가세'),
        max_digits=100,
        decimal_places=4,
        null=True,
        blank=True,
    )
    group_manage = models.CharField(
        verbose_name=_('관리 항목'),
        max_length=100,
        null=True,
        blank=True,
    )
    info = models.CharField(
        verbose_name=_('품목 정보'),
        max_length=100,
        null=True,
        blank=True,
    )
    memo = models.CharField(
        verbose_name=_('메모'),
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('주문 2_품목')
        verbose_name_plural = _('주문 2_품목')

    def __str__(self):
        return '{} {} {}'.format(self.name, self.standard, self.memo,)

class OrderImg(TimeStampedModel):
    order_list = models.ForeignKey(
        'design.OrderList',
        verbose_name=_('주문 품목'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )
    # 업로드하는 시안과 추가 업로드하는 시안이 수정된 시안이라고 연결해주는 숫자
    order_img_num = models.IntegerField(
        verbose_name=_('이미지 넘버링'),
        null=True,
        blank=True,
    )
    sample = models.CharField(
        verbose_name=_('샘플명'),
        max_length=100,
        null=True,
        blank=True,
    )
    # 연결된 이미지의 구분값  1-수정완료 > 1-수정완료 > 1-대기
    IMG_STATE_WHAT = Choices(
        (0, '대기', _('대기')),
        (1, '수정완료', _('수정완료')),
        (2, '확정', _('확정')),
        (3, '보류', _('보류')),
        (4, '취소', _('취소')),
        (5, '무효처리', _('무효처리')),
    )
    state = models.IntegerField(
        verbose_name=_('시안 상태'),
        choices=IMG_STATE_WHAT,
        null=True,
        blank=True,
        default=0,
    )

    def upload_to_order(instance, filename):
        now = datetime.now()
        nowDate = now.strftime('%Y%m')
        return 'order/{}{}/{}'.format(nowDate ,instance.order_list.order_info.profile.user, filename)

    sample_img = models.ImageField(
        verbose_name=_('order_img'),
        blank=True,
        upload_to=upload_to_order,
    )

    class Meta:
        verbose_name = _('주문 3_시안')
        verbose_name_plural = _('주문 3_시안')

    def __str__(self):
        return '{} {} {}'.format(self.order_list.order_info.profile.company,self.sample, self.state)

class OrderMemo(TimeStampedModel):
    order_img = models.ForeignKey(
        'design.OrderImg',
        verbose_name=_('주문 이미지'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )
    check = models.BooleanField(
        verbose_name=_('확인'),
        default=False,
    )
    memo = models.CharField(
        verbose_name=_('내용'),
        max_length= 9000,
        blank=True,
        null=True,
    )
    location = models.CharField(
        verbose_name=_('위치 좌표'),
        max_length=9000,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('주문 4_시안 메모')
        verbose_name_plural = _('주문 4_시안 메모')

    def __str__(self):
        return '{} {} {}'.format(self.order_img,self.check,self.memo,)