import re
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from datetime import datetime, timedelta

class Profile(TimeStampedModel):
    PHONE_VERIFIED_STATUS_CHOICES = Choices(
        (0, 'unverified', _('본인인증 X')),
        (1, 'verified', _('본인인증 O')),
        (2, 'revoked', _('본인인증 취소'))
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    division = models.IntegerField(
        verbose_name=_('구분 판매처=1 매입처=2'),
        default= 1 ,
        blank=True,
        null=True,
    )

    code = models.IntegerField(
        verbose_name=_('사업자번호'),
        unique = True,
        null=True,
    )

    company = models.CharField(
        verbose_name=_('업체명'),
        max_length=255,
        blank=True,
    )
    company_keyword = models.CharField(
        verbose_name=_('검색창 내용/ 키워드'),
        max_length=255,
        blank=True,
    )

    ceo = models.CharField(
        verbose_name=_('대표자명'),
        max_length=255,
        blank=True,
    )

    tax_bill_mail = models.CharField(
        verbose_name=_('이메일'),
        max_length=255,
        blank=True,
    )

    sectors = models.CharField(
        verbose_name=_('업종'),
        max_length=255,
        blank=True,
    )

    business = models.CharField(
        verbose_name=_('업태'),
        max_length=255,
        blank=True,
    )

    tell = models.CharField(
        verbose_name=_('매장번호'),
        max_length=255,
        blank=True,
    )

    keywords = models.CharField(
        verbose_name=_('키워드'),
        max_length=1000,
        blank=True,
    )

    memo = models.CharField(
        verbose_name=_('메모'),
        max_length=255,
        blank=True,
    )

    phone = models.CharField(
        verbose_name=_('phone number'),
        max_length=17,
        blank=True,
        null=True,
    )

    address = models.CharField(
        verbose_name=_('주소'),
        max_length=255,
        blank=True,
    )

    address2 = models.CharField(
        verbose_name=_('주소2'),
        max_length=255,
        blank=True,
    )

    phone_verified = models.BooleanField(
        verbose_name=_('phone verified'),
        default=False,
    )

    phone_verified_status = models.IntegerField(
        verbose_name=_('cellphone verified status'),
        choices=PHONE_VERIFIED_STATUS_CHOICES,
        default=PHONE_VERIFIED_STATUS_CHOICES.unverified,
        db_index=True,
    )

    date_of_birth = models.DateField(
        verbose_name=_('date of birth'),
        blank=True,
        null=True,
    )

    options = models.CharField(
        verbose_name=_('결재/포함/택배'),
        max_length=255,
        blank=True,
    )

    confirm = models.CharField(
        verbose_name=_('시안 확인'),
        max_length=255,
        blank=True,
    )

    discount = models.CharField(
        verbose_name=_('할인율'),
        max_length=255,
        blank=True,
    )

    api_state = models.IntegerField(
        verbose_name=_('api_state'),
        default=0,
        blank=True,
        null=True,
    )

    manager = models.CharField(
        verbose_name = _('담당자'),
        max_length=100,
        null=True,
        blank=True,
    )
    state = models.CharField(
        verbose_name=_('사업자 상태'),
        max_length=100,
        null=True,
        blank=True,
    )
    STATE_SELECT = Choices(
        (0, '정상', _('정상')),
        (1, '폐업', _('폐업')),
    )
    state_select = models.IntegerField(
        verbose_name=_('사업자 상태'),
        choices= STATE_SELECT,
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return '{} ( {} ) / {}'.format(self.company, self.company_keyword, self.user.username)

    @property
    def full_name(self):
        # Only Hangul
        pattern = re.compile(r'^[가-힣]+$')

        if pattern.match(self.user.last_name) and pattern.match(self.user.first_name):
            return '{}{}'.format(self.user.last_name, self.user.first_name)
        else:
            return '{} {}'.format(self.user.first_name, self.user.last_name)

    full_name.fget.short_description = _('Full name')

    @property
    def email(self):
        return self.user.email

    email.fget.short_description = _('E-mail')

class LoginLog(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_owned",
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP address'),
    )

    class Meta:
        verbose_name = _('login log')
        verbose_name_plural = _('login logs')

    def __str__(self):
        return '{} {} {}'.format(self.user.email, self.ip_address, self.created)

class PhoneVerificationLog(models.Model):
    GENDER_CHOICES = Choices(
        (0, 'female', _('female')),
        (1, 'male', _('male')),
    )

    DOMESTIC_CHOICES = Choices(
        (0, 'foreign', _('foreign')),
        (1, 'domestic', _('domestic')),
    )

    token = models.CharField(
        verbose_name=_('token'),
        max_length=255,
        blank=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        related_name="phone_verification_logs",
    )

    code = models.CharField(
        verbose_name=_('code'),
        max_length=32,
        blank=True,
    )

    reason = models.CharField(
        verbose_name=_('reason'),
        max_length=16,
        blank=True,
    )

    result_code = models.CharField(
        verbose_name=_('result code'),
        max_length=16,
        blank=True,
    )

    message = models.CharField(
        verbose_name=_('message'),
        max_length=255,
        blank=True,
    )

    transaction_id = models.CharField(
        verbose_name=_('transaction id'),
        max_length=32,
        blank=True,
    )

    di = models.CharField(
        verbose_name=_('di'),
        max_length=255,
        blank=True,
    )

    ci = models.TextField(
        verbose_name=_('ci'),
        blank=True,
    )

    fullname = models.CharField(
        verbose_name=_('fullname'),
        max_length=32,
        blank=True,
    )

    date_of_birth = models.CharField(
        verbose_name=_('date of birth'),
        max_length=16,
        blank=True,
    )

    gender = models.IntegerField(
        verbose_name=_('gender'),
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES.male,
        db_index=True,
    )

    domestic = models.IntegerField(
        verbose_name=_('domestic'),
        choices=DOMESTIC_CHOICES,
        default=DOMESTIC_CHOICES.domestic,
        db_index=True,
    )

    telecom = models.CharField(
        verbose_name=_('telecom'),
        max_length=16,
        blank=True,
    )

    cellphone = models.CharField(
        verbose_name=_('cellphone'),
        max_length=32,
        blank=True,
    )

    return_message = models.CharField(
        verbose_name=_('return_message'),
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = _('phone verification log')
        verbose_name_plural = _('phone verification logs')

    def __str__(self):
        return '{} {}'.format(self.fullname, self.cellphone)

