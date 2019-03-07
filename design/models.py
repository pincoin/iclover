import re

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from member.models import *
from datetime import datetime, timedelta

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
        verbose_name = _('상품 배너')
        verbose_name_plural = _('상품 배너')

    def __str__(self):
        return '{} / {}'.format(self.get_category_display(), self.subtitle)