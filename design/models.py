import uuid
import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import SoftDeletableModel, TimeStampedModel
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel


class Category(TimeStampedModel, SoftDeletableModel, MPTTModel):
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


class SectorsCategory(TimeStampedModel, SoftDeletableModel, MPTTModel):
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

    objects = TreeManager()

    def __str__(self):
        return self.title


class Option(TimeStampedModel, SoftDeletableModel, MPTTModel):
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

class ProductBase(TimeStampedModel, SoftDeletableModel):
    category = models.ForeignKey(
        'design.Category',
        verbose_name=_('카테고리'),
        related_name='product_base_category',
        null=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    supplier = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('매입처'),
        blank= True,
    )

    standard = models.ManyToManyField(
        'design.StandardOption',
        related_name='product_base_standard',
        blank=True,
    )

    paper = models.ManyToManyField(
        'design.PaperOption',
        related_name='product_base_paper',
        blank=True,
    )

    side = models.ManyToManyField(
        'SideOption',
        related_name='product_base_side',
        blank=True,
    )

    etc = models.ManyToManyField(
        'design.EtcOption',
        related_name='product_base_etc',
        blank=True,
    )

    code = models.IntegerField(
        verbose_name=_('품목코드'),
        null=True,
        blank=True,
    )

    title = models.CharField(
        verbose_name=_('품목명'),
        null=True,
        blank=True,
        max_length=128,
    )

    slug = models.SlugField(
        verbose_name=_('slug'),
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        allow_unicode=True,
    )

    sell_price = models.DecimalField(
        verbose_name=_('판매가'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )

    buy_price = models.DecimalField(
        verbose_name=_('매입가'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )

    main_quantity = models.BooleanField(
        verbose_name=_('메인 수량'),
        default = False,
    )

    ecount = models.BooleanField(
        verbose_name=_('이카운트 전송'),
        default=False,
    )

    product_active = models.BooleanField(
        verbose_name=_('활성화'),
        default = False,
    )

    class Meta:
        verbose_name = _('상품옵션_통합')
        verbose_name_plural = _('상품옵션_통합')

    def __str__(self):
        return self.title

class ProductText(TimeStampedModel, SoftDeletableModel):
    category = models.ForeignKey(
        'design.Category',
        verbose_name=_('카테고리'),
        blank=True,
        null=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    supplier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name=_('매입처'),
        blank=True,
        null=True,
    )

    standard = models.CharField(
        max_length=255,
        verbose_name=_('규격명'),
        null=True,
        blank= True,
    )
    horizontal = models.DecimalField(
        verbose_name=_('가로'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )
    vertical = models.DecimalField(
        verbose_name=_('세로'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )
    width = models.DecimalField(
        verbose_name=_('넓이'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )
    height = models.DecimalField(
        verbose_name=_('높이'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )

    paper = models.CharField(
        verbose_name=_('재질'),
        max_length=255,
        blank=True,
        null=True,

    )

    gram = models.CharField(
        verbose_name=_('그람수'),
        blank=True,
        null=True,
        max_length=100,
    )

    color = models.CharField(
        verbose_name=_('색상'),
        blank=True,
        null=True,
        max_length=100,
    )

    paper_option = models.CharField(
        verbose_name=_('옵션 코팅/유무'),
        blank=True,
        null=True,
        max_length=100,
    )

    side = models.CharField(
        verbose_name=_('양면 / 단면'),
        blank=True,
        null=True,
        max_length=100,
    )

    etc = models.CharField(
        verbose_name=_('기타 정보'),
        blank=True,
        null=True,
        max_length=100,
    )
    etc_option = models.CharField(
        verbose_name=_('기타 옵션 상세'),
        blank=True,
        null=True,
        max_length=100,
    )

    memo = models.CharField(
        verbose_name=_('기타 옵션 메모'),
        blank=True,
        null=True,
        max_length=100,
    )

    code = models.IntegerField(
        verbose_name=_('품목코드'),
        null=True,
        blank=True,
    )

    title = models.CharField(
        verbose_name=_('품목명'),
        null=True,
        blank=True,
        max_length=128,
    )

    slug = models.SlugField(
        verbose_name=_('slug'),
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        allow_unicode=True,
    )

    sell_price = models.DecimalField(
        verbose_name=_('판매가'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )

    buy_price = models.DecimalField(
        verbose_name=_('매입가'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )

    quantity = models.DecimalField(
        verbose_name=_('메인 수량'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )

    main_quantity = models.BooleanField(
        verbose_name=_('메인 수량'),
        default = False,
    )

    ecount = models.BooleanField(
        verbose_name=_('이카운트 전송'),
        default=True,
    )

    product_active = models.BooleanField(
        verbose_name=_('활성화'),
        default = False,
    )
    product_version = models.IntegerField(
        verbose_name=_('version'),
        blank=True,
        null=True,
    )
    group = models.IntegerField(
        verbose_name=_('group'),
        blank=True,
        null=True,
    )

    @property
    def benefit(self):
        if self.sell_price and self.buy_price:
            data = 0
            try:
                data = self.buy_price / self.sell_price * 100
                data = 100-data
                return data
            except:
                return data

    class Meta:
        verbose_name = _('상품옵션_통합 str')
        verbose_name_plural = _('상품옵션_통합 str')

    def __str__(self):
        return self.title


class StandardOption(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(
        verbose_name=_('품목명'),
        blank=True,
        null=True,
        max_length=100,
    )
    horizontal = models.DecimalField(
        verbose_name=_('가로'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )
    vertical = models.DecimalField(
        verbose_name=_('세로'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )
    width = models.DecimalField(
        verbose_name=_('넓이'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )
    height = models.DecimalField(
        verbose_name=_('높이'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('상품옵션 _기본 규격')
        verbose_name_plural = _('상품옵션 _기본 규격')

    def __str__(self):
        return self.title

class PaperOption(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(
        verbose_name=_('용지 이름'),
        blank = True,
        null = True,
        max_length=100,
    )

    gram = models.CharField(
        verbose_name=_('그람수'),
        blank=True,
        null=True,
        max_length=100,
    )

    color = models.CharField(
        verbose_name=_('색상'),
        blank=True,
        null=True,
        max_length=100,
    )

    option = models.CharField(
        verbose_name=_('옵션 코팅/유무'),
        blank=True,
        null=True,
        max_length=100,
    )

    class Meta:
        verbose_name = _('상품옵션 _용지옵션')
        verbose_name_plural = _('상품옵션 _용지옵션')

    def __str__(self):
        return self.title


class SideOption(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(
        verbose_name=_('양면 / 단면'),
        blank=True,
        null=True,
        max_length=100,
    )

    class Meta:
        verbose_name = _('상품옵션 _양면/단면')
        verbose_name_plural = _('상품옵션 _양면/단면')

    def __str__(self):
        return self.title

class HooOption(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(
        verbose_name=_('후가공명'),
        blank=True,
        null=True,
        max_length=100,
    )
    option = models.CharField(
        verbose_name=_('상위 품목'),
        blank=True,
        null=True,
        max_length=100,
    )

    price = models.DecimalField(
        verbose_name=_('후가공 가격'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('상품옵션 _후가공')
        verbose_name_plural = _('상품옵션 _후가공')

    def __str__(self):
        return self.title

class DeliveryOption(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(
        verbose_name=_('배송 방법'),
        blank=True,
        null=True,
        max_length=100,
    )

    price = models.DecimalField(
        verbose_name=_('배송 비용'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )

    tax = models.BooleanField(
        verbose_name=_('부가세 포함여부'),
        default = False,
    )

    class Meta:
        verbose_name = _('상품옵션 _배송비')
        verbose_name_plural = _('상품옵션 _배송비')

    def __str__(self):
        return self.title

class EtcOption(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(
        verbose_name=_('기타 옵션'),
        blank=True,
        null=True,
        max_length=255,
    )
    option = models.CharField(
        verbose_name=_('기타 옵션 상세'),
        blank=True,
        null=True,
        max_length=255,
    )

    memo = models.CharField(
        verbose_name=_('기타 옵션 메모'),
        blank=True,
        null=True,
        max_length=255,
    )

    price = models.DecimalField(
        verbose_name=_('기타 옵션 가격'),
        max_digits=11,
        decimal_places=4,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('상품옵션 _기타옵션')
        verbose_name_plural = _('상품옵션 _기타옵션')

    def __str__(self):
        return self.title


class OrderInfo(TimeStampedModel, SoftDeletableModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('거래처'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    today_num = models.IntegerField(
        verbose_name=_('today-넘버링'),
        default=1,
    )

    joo_date = models.DateField(
        verbose_name=_('주문일'),
        null=True,
        blank=True,
    )

    order_date = models.DateField(
        verbose_name=_('발주일'),
        null=True,
        blank=True,
    )

    company = models.CharField(
        verbose_name=_('업체명'),
        max_length=255,
        null=True,
        blank=True,
    )
    company_keyword = models.CharField(
        verbose_name=_('업체 키워드'),
        max_length=255,
        null=True,
        blank=True,
    )

    address = models.CharField(
        verbose_name=_('주소'),
        max_length=255,
        null=True,
        blank=True,
    )
    tell = models.CharField(
        verbose_name=_('연락처'),
        max_length=255,
        null=True,
        blank=True,
    )

    STATE_WHAT = Choices(
        (0, '견적', _('견적')),
        (1, '주문', _('주문')),
        (2, '시안', _('시안')),
        (3, '제작', _('제작')),
        (4, '완료', _('완료')),
        (5, '취소', _('취소')),
        (6, '보류', _('보류')),
        (7, '환불', _('환불')),
        (8, '입금대기', _('입금대기')),
    )

    state = models.IntegerField(
        verbose_name=_('상태값'),
        choices=STATE_WHAT,
        default=0,
        blank=True,
        db_index=True,
    )


    tax = models.BooleanField(
        verbose_name=_('부가세포함'),
        default=True,
    )

    keywords = models.CharField(
        verbose_name=_('검색창 내용'),
        max_length=1000,
        null=True,
        blank=True,
    )

    checker = models.CharField(
        verbose_name=_('시안 확인'),
        max_length=255,
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
        max_length=255,
        null=True,
        blank=True,
    )

    employees = models.CharField(
        verbose_name=_('작업자'),
        null=True,
        blank=True,
        max_length=100,
        db_index=True,
    )

    fix_manager = models.CharField(
        verbose_name=_('담당자'),
        null=True,
        blank=True,
        max_length=100,
        db_index=True,
    )

    in_memo = models.CharField(
        verbose_name=_('관리자메모'),
        max_length=255,
        null=True,
        blank=True,
    )

    out_memo = models.CharField(
        verbose_name=_('고객표시 메모'),
        max_length=255,
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
        return '{} {} {}'.format(self.user, self.company, self.employees)


class OrderList(TimeStampedModel, SoftDeletableModel):
    order_info = models.ForeignKey(
        'design.OrderInfo',
        verbose_name=_('주문 정보'),
        related_name= 'order_list',
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
    num = models.IntegerField(
        verbose_name=_('동일 전표'),
        null=True,
        blank=True,
    )
    code = models.IntegerField(
        verbose_name=_('품목코드'),
        null=True,
        blank=True,
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
        max_digits=11,
        decimal_places=4,
        default=0,
        null=True,
        blank=True,
    )
    price_tax = models.DecimalField(
        verbose_name=_('매입 부가세'),
        max_digits=11,
        decimal_places=4,
        default=0,
        null=True,
        blank=True,
    )
    selling_price = models.DecimalField(
        verbose_name=_('판매가'),
        max_digits=11,
        decimal_places=4,
        default=0,
        null=True,
        blank=True,
    )
    selling_price_tax = models.DecimalField(
        verbose_name=_('판매 부가세'),
        max_digits=11,
        decimal_places=4,
        default=0,
        null=True,
        blank=True,
    )
    group_manage = models.CharField(
        verbose_name=_('관리 항목'),
        max_length=100,
        null=True,
        blank=True,
    )
    gram = models.CharField(
        verbose_name=_('기타'),
        max_length=100,
        null=True,
        blank=True,
    )

    etc = models.CharField(
        verbose_name=_('적요'),
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
        return '{} {} {}'.format(self.name, self.standard, self.memo, )


class OrderImg(TimeStampedModel, SoftDeletableModel):
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
        return 'order/{}/{}/{}'.format(instance.order_list.order_info.user, nowDate, filename)

    order_img = models.ImageField(
        verbose_name=_('order_img'),
        blank=True,
        upload_to=upload_to_order,
    )

    class Meta:
        verbose_name = _('주문 3_시안')
        verbose_name_plural = _('주문 3_시안')

    def __str__(self):
        return '{} {}'.format(self.sample, self.state)


class OrderMemo(TimeStampedModel, SoftDeletableModel):
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
        max_length=9000,
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
        return '{} {} {}'.format(self.order_img, self.check, self.memo, )
