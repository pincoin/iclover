import uuid
import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from model_utils import Choices
from model_utils.models import SoftDeletableModel, TimeStampedModel
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from pilkit.processors import ResizeToFit


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

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        verbose_name = _('카테고리 품목')
        verbose_name_plural = _('카테고리 품목')

    def __str__(self):
        return f'{self.title}'


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

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        verbose_name = _('카테고리 업종')
        verbose_name_plural = _('카테고리 업종')

    objects = TreeManager()

    def __str__(self):
        return f'{self.title}'


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
        return f'{self.title}'

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
        default=0,
        null=True,
        blank=True,
    )
    vertical = models.DecimalField(
        verbose_name=_('세로'),
        max_digits=11,
        decimal_places=4,
        default=0,
        null=True,
        blank=True,
    )
    width = models.DecimalField(
        verbose_name=_('넓이'),
        max_digits=11,
        decimal_places=4,
        default=0,
        null=True,
        blank=True,
    )
    height = models.DecimalField(
        verbose_name=_('높이'),
        max_digits=11,
        decimal_places=4,
        default=0,
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
        default=0,
        null=True,
        blank=True,
    )

    buy_price = models.DecimalField(
        verbose_name=_('매입가'),
        max_digits=11,
        decimal_places=4,
        default=0,
        null=True,
        blank=True,
    )

    quantity = models.DecimalField(
        verbose_name=_('메인 수량'),
        max_digits=11,
        decimal_places=4,
        default=0,
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
        default=1,
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
        return f'{self.title}'

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
        (9, '배송', _('배송')),
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
        max_length=1000,
        null=True,
        blank=True,
    )

    out_memo = models.CharField(
        verbose_name=_('고객표시 메모'),
        max_length=1000,
        null=True,
        blank=True,
    )

    deposit_check = models.IntegerField(
        verbose_name=_('입금 확인 및 차액'),
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
        return f'{self.user} {self.company} {self.employees}'

class OrderList(TimeStampedModel):
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
        max_length=1000,
        null=True,
        blank=True,
    )
    standard = models.CharField(
        verbose_name=_('규격'),
        max_length=1000,
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
        max_length=1000,
        null=True,
        blank=True,
    )
    gram = models.CharField(
        verbose_name=_('기타'),
        max_length=1000,
        null=True,
        blank=True,
    )

    etc = models.CharField(
        verbose_name=_('적요'),
        max_length=1000,
        null=True,
        blank=True,
    )
    memo = models.CharField(
        verbose_name=_('메모'),
        max_length=2000,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('주문 2_품목')
        verbose_name_plural = _('주문 2_품목')

    def __str__(self):
        return f'{self.name} {self.standard} {self.memo}'

    @property
    def total(self):
        data1 = round(self.selling_price)*self.quantity
        data2 = round(self.selling_price_tax)*self.quantity
        data = data1+data2
        return data

class OrderImg(TimeStampedModel, SoftDeletableModel):
    order_info = models.ForeignKey(
        'design.CustomerOrderInfo',
        verbose_name=_('주문 리스트'),
        related_name='order_img',
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )
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
    # 업로드하는 시안과 추가 업로드하는 시안이 수정된 시안이라고 연결해주는 숫자
    employees = models.CharField(
        verbose_name=_('업로더'),
        max_length=255,
        null=True,
        blank=True,
    )

    order_img_num = models.IntegerField(
        verbose_name=_('이미지 넘버링'),
        null=True,
        blank=True,
    )
    plush_date = models.DateTimeField(
        verbose_name=_('등록일'),
        auto_now_add=True,
    )

    name = models.CharField(
        verbose_name=_('제목'),
        max_length=255,
        blank=True,
    )

    keyword = models.CharField(
        verbose_name=_('키워드'),
        max_length=255,
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
    state_at = models.IntegerField(
        verbose_name=_('시안 상태'),
        choices=IMG_STATE_WHAT,
        null=True,
        blank=True,
        default=0,
    )
    state = models.BooleanField(
        verbose_name=_('노출 상태'),
        default=True,
    )

    def upload_to_order(instance, filename):
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y%m')
        return f'order/{instance.order_info.user}/{nowDate}/{filename}'

    images = ProcessedImageField(
        verbose_name=_('sample_img'),
        processors=[ResizeToFit(600, 600)],
        blank=True,
        upload_to=upload_to_order,
    )

    link = models.CharField(
        verbose_name=_('링크 url'),
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = _('주문 3_시안')
        verbose_name_plural = _('주문 3_시안')

    def __str__(self):
        return f'{self.name} {self.state}'


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
        return f'{self.order_img} {self.check} {self.memo}'

class MainImg(TimeStampedModel):
    IMG_KIND = Choices(
        (0, '메인 배너', _('메인 배너')),
        (1, '중간 목업', _('중간 목업')),
    )
    state_at = models.IntegerField(
        verbose_name=_('이미지 구분'),
        choices=IMG_KIND,
        null=True,
        blank=True,
    )
    kind = models.CharField(
        verbose_name=_('품목 종류'),
        max_length=255,
        blank=True,
    )

    name = models.CharField(
        verbose_name=_('name of product'),
        max_length=255,
        blank=True,
    )

    origin_url = models.CharField(
        verbose_name=_('샘플 원본 url'),
        max_length=255,
        blank=True,
    )

    active = models.BooleanField(
        default=True
    )

    def upload_to_product(instance, filename):
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y')
        return f'product/{nowDate}/{filename}'

    banner_img = models.ImageField(
        verbose_name=_('banner_img'),
        blank= True,
        upload_to= upload_to_product,
    )

    class Meta:
        verbose_name = _('메인 배너')
        verbose_name_plural = _('메인 배너')

    def __str__(self):
        return f'{self.name}'


class ProductImg(TimeStampedModel):
    name = models.CharField(
        verbose_name=_('slug'),
        max_length=255,
        blank=True,
    )

    keyword = models.CharField(
        verbose_name=_('키워드'),
        max_length=255,
        blank=True,
    )

    def upload_to_product_default_img(instance, filename):
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y')
        return f'product_default_img/{nowDate}/{filename}'

    images = models.ImageField(
        verbose_name=_('product_default_img'),
        null=True,
        blank=True,
        upload_to=upload_to_product_default_img,
    )

    def save(self, request=False, *args, **kwargs):
        super(ProductImg, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('기본 이미지')
        verbose_name_plural = _('기본 이미지')

    def __str__(self):
        return f'{self.name}'

class CartProduct(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name=_('고객'),
        blank=True,
        null=True,
    )
    json_text = models.CharField(
        verbose_name=_('json data'),
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('카트 json 텍스트')
        verbose_name_plural = _('카트 json 텍스트')

    def __str__(self):
        return f'{self.user}'

class CartPriceProblem(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name=_('고객'),
        blank=True,
        null=True,
    )
    json_text = models.CharField(
        verbose_name=_('json data'),
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('카트 가격 변동 json 텍스트')
        verbose_name_plural = _('카트 가격 변동 json 텍스트')

    def __str__(self):
        return f'{self.user}'

class DeliveryPrice(TimeStampedModel):
    kind = models.CharField(
        verbose_name=_('품목 종류'),
        max_length=255,
        blank=True,
        null=True
    )
    size = models.CharField(
        verbose_name=_('규격 size'),
        max_length=255,
        blank=True,
        null=True
    )
    paper = models.CharField(
        verbose_name=_('용지 paper'),
        max_length=255,
        blank=True,
        null=True
    )
    side = models.CharField(
        verbose_name=_('인쇄 side'),
        max_length=255,
        blank=True,
        null=True
    )
    deal = models.CharField(
        verbose_name=_('수량 deal'),
        max_length=255,
        blank=True,
        null=True
    )
    supplier = models.CharField(
        verbose_name=_('매입'),
        max_length=255,
        blank=True,
        null=True
    )
    memo = models.CharField(
        verbose_name=_('메모 memo'),
        max_length=255,
        blank=True,
        null=True
    )
    sell = models.DecimalField(
        verbose_name=_('sell'),
        blank=True,
        default=0,
        decimal_places=4,
        max_digits=11,
    )
    buy_price = models.DecimalField(
        verbose_name=_('buy'),
        blank=True,
        default=0,
        decimal_places=4,
        max_digits=11,
    )
    class Meta:
        verbose_name = _('고객 배송비')
        verbose_name_plural = _('고객 배송비')

    def __str__(self):
        return f'{self.size} 배송비 : {self.sell}'


class ProductPriceAPI(TimeStampedModel):
    kind = models.CharField(
        verbose_name=_('품목 종류'),
        max_length=255,
        blank=True,
        null=True
    )
    title = models.CharField(
        verbose_name=_('품목 종류 한글'),
        max_length=255,
        blank=True,
        null=True
    )
    size = models.CharField(
        verbose_name=_('규격 size'),
        max_length=255,
        blank=True,
        null=True
    )
    size_text = models.CharField(
        verbose_name=_('규격 size text'),
        max_length=255,
        blank=True,
        null=True
    )
    paper = models.CharField(
        verbose_name=_('용지 paper'),
        max_length=255,
        blank=True,
        null=True
    )
    paper_text = models.CharField(
        verbose_name=_('용지 paper text'),
        max_length=255,
        blank=True,
        null=True
    )
    side = models.CharField(
        verbose_name=_('인쇄 side'),
        max_length=255,
        blank=True,
        null=True
    )
    side_text = models.CharField(
        verbose_name=_('인쇄 side text'),
        max_length=255,
        blank=True,
        null=True
    )
    deal = models.CharField(
        verbose_name=_('수량 deal'),
        max_length=255,
        blank=True,
        null=True
    )
    deal_text = models.CharField(
        verbose_name=_('수량 deal text'),
        max_length=255,
        blank=True,
        null=True
    )
    option1 = models.CharField(
        verbose_name=_('옵션1 option1'),
        max_length=255,
        blank=True,
        null=True
    )
    option1_text = models.CharField(
        verbose_name=_('옵션1 option1 text'),
        max_length=255,
        blank=True,
        null=True
    )
    option2 = models.CharField(
        verbose_name=_('옵션1 option2'),
        max_length=255,
        blank=True,
        null=True
    )
    option2_text = models.CharField(
        verbose_name=_('옵션1 option2 text'),
        max_length=255,
        blank=True,
        null=True
    )

    sell = models.DecimalField(
        verbose_name=_('sell'),
        blank=True,
        default=0,
        decimal_places=4,
        max_digits=11,
    )
    supplier = models.CharField(
        verbose_name=_('매입'),
        max_length=255,
        blank=True,
        null=True
    )
    memo = models.CharField(
        verbose_name=_('메모 memo'),
        max_length=255,
        blank=True,
        null=True
    )
    buy_price = models.DecimalField(
        verbose_name=_('buy'),
        blank=True,
        default=0,
        decimal_places=4,
        max_digits=11,
    )

    class Meta:
        verbose_name = _('가격 리턴 api')
        verbose_name_plural = _('가격 리턴 api')

    def __str__(self):
        return f'{self.size}'

class CustomerOrderInfo(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name=_('고객'),
        blank=True,
        null=True,
    )
    joo_date = models.DateField(
        verbose_name=_('주문일'),
        null=True,
        blank=True,
        default=datetime.date.today
    )
    order_date = models.DateField(
        verbose_name=_('발주일'),
        null=True,
        blank=True,
    )
    company = models.CharField(
        verbose_name=_('회사명'),
        max_length=255,
        blank=True,
        null=True
    )
    uuid = models.CharField(
        verbose_name=_('uuid'),
        max_length=255,
        blank=True,
        null=True
    )
    code = models.IntegerField(
        verbose_name=_('사업자번호'),
        null=True,
        blank=True,
    )
    phone = models.CharField(
        verbose_name=_('폰 번호'),
        max_length=255,
        null=True,
        blank=True,
    )

    address_confirm = models.BooleanField(
        default=True
    )

    address = models.CharField(
        verbose_name=_('주소'),
        max_length=255,
        null=True,
        blank=True,
    )

    address2 = models.CharField(
        verbose_name=_('주소2'),
        max_length=255,
        null=True,
        blank=True,
    )

    address_detail = models.CharField(
        verbose_name=_('상세주소'),
        max_length=255,
        null=True,
        blank=True,
    )

    address_option = models.CharField(
        verbose_name=_('주소 참고'),
        max_length=255,
        null=True,
        blank=True,
    )

    BILL_SELECT = Choices(
        (0, '세금계산서', _('세금계산서')),
        (1, '사업자 지출증빙', _('사업자 지출증빙')),
        (2, '현금 영수증', _('현금 영수증')),
        (3, '미발행', _('미발행')),
    )

    bill_select = models.IntegerField(
        verbose_name=_('사업자 상태'),
        choices=BILL_SELECT,
        null=True,
        blank=True,
    )

    STATE_SELECT = Choices(
        (0, '주문 확인중', _('주문 확인중')),
        (1, '입금대기', _('입금대기')),
        (2, '시안 중', _('시안 중')),
        (3, '제작 중', _('제작 중')),
        (4, '배송 중', _('배송 중')),
        (5, '완료', _('완료')),
        (6, '취소', _('취소')),
        (7, '보류', _('보류')),
        (8, '재인쇄', _('재인쇄')),
    )
    state = models.IntegerField(
        verbose_name=_('주문서 상태'),
        choices=STATE_SELECT,
        default=0,
        null=True,
        blank=True,
    )
    num = models.IntegerField(
        verbose_name=_('하루 주문 카운트'),
        default=1,
    )
    show_memo = models.CharField(
        verbose_name=_('고객 노출 메모'),
        max_length=255,
        null=True,
        blank=True,
    )
    inside_memo = models.CharField(
        verbose_name=_('내부 메모'),
        max_length=255,
        null=True,
        blank=True,
    )
    manager = models.CharField(
        verbose_name=_('작업자'),
        max_length=255,
        null=True,
        blank=True,
    )
    fix_manager = models.CharField(
        verbose_name=_('고정 담당자'),
        max_length=255,
        null=True,
        blank=True,
    )
    confirm = models.CharField(
        verbose_name=_('시안 확인'),
        max_length=255,
        null=True,
        blank=True,
    )
    hoo = models.CharField(
        verbose_name=_('기타 정보'),
        max_length=255,
        null=True,
        blank=True,
    )

    tax_bool = models.BooleanField(
        verbose_name=_('부가세 정보'),
        default=True
    )

    deposit_state = models.BooleanField(
        verbose_name=_('입금 컨펌'),
        default=False
    )
    deposit_price = models.IntegerField(
        verbose_name=_('차액'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('고객 주문 기본 정보')
        verbose_name_plural = _('고객 주문 기본 정보')

    def __str__(self):
        return f'{self.uuid} {self.company}'

class CustomerOrderProduct(TimeStampedModel):
    customer_order_info = models.ForeignKey(
        'design.CustomerOrderInfo',
        blank=True,
        null=True,
        related_name='customer_order_product',
        verbose_name=_('고객 주문 정보'),
        db_index=True,
        on_delete=models.SET_NULL,
    )

    name = models.CharField(
        verbose_name=_('보여질 품목명'),
        max_length=255,
        blank=True,
        null=True
    )

    ordering = models.IntegerField(
        default=1
    )

    kind = models.CharField(
        verbose_name=_('품목 종류 kind'),
        max_length=255,
        blank=True,
        null=True
    )
    title = models.CharField(
        verbose_name=_('품목 종류 title'),
        max_length=255,
        blank=True,
        null=True
    )
    size = models.CharField(
        verbose_name=_('규격 size'),
        max_length=255,
        blank=True,
        null=True
    )
    size_text = models.CharField(
        verbose_name=_('규격 size text'),
        max_length=255,
        blank=True,
        null=True
    )
    paper = models.CharField(
        verbose_name=_('용지 paper'),
        max_length=255,
        blank=True,
        null=True
    )
    paper_text = models.CharField(
        verbose_name=_('용지 paper text'),
        max_length=255,
        blank=True,
        null=True
    )
    side = models.CharField(
        verbose_name=_('인쇄 side'),
        max_length=255,
        blank=True,
        null=True
    )
    side_text = models.CharField(
        verbose_name=_('인쇄 side text'),
        max_length=255,
        blank=True,
        null=True
    )
    deal = models.CharField(
        verbose_name=_('수량 deal'),
        max_length=255,
        blank=True,
        null=True
    )
    deal_text = models.CharField(
        verbose_name=_('수량 deal text'),
        max_length=255,
        blank=True,
        null=True
    )
    option1 = models.CharField(
        verbose_name=_('옵션1 option1'),
        max_length=255,
        blank=True,
        null=True
    )
    option1_text = models.CharField(
        verbose_name=_('옵션1 option1 text'),
        max_length=255,
        blank=True,
        null=True
    )
    option2 = models.CharField(
        verbose_name=_('옵션1 option2'),
        max_length=255,
        blank=True,
        null=True
    )
    option2_text = models.CharField(
        verbose_name=_('옵션1 option2 text'),
        max_length=255,
        blank=True,
        null=True
    )
    sell = models.DecimalField(
        verbose_name=_('sell'),
        blank=True,
        default=0,
        decimal_places=4,
        max_digits=11,
    )
    buy_price = models.DecimalField(
        verbose_name=_('buy'),
        blank=True,
        default=0,
        decimal_places=4,
        max_digits=11,
    )
    amount = models.IntegerField(
        verbose_name=_('건수'),
        default=1,
        blank=True,
    )
    supplier = models.CharField(
        verbose_name=_('supplier'),
        max_length=255,
        blank=True,
        null=True
    )
    memo = models.CharField(
        verbose_name=_('memo'),
        max_length=255,
        blank=True,
        null=True
    )
    etc = models.CharField(
        verbose_name=_('etc'),
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('고객 주문 품목')
        verbose_name_plural = _('고객 주문 품목')
        ordering = ['ordering']

    def __str__(self):
        return f'{self.size}'