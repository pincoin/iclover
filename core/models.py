import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class AbstractPage(TimeStampedModel):
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )

    description = models.CharField(
        verbose_name=_('description'),
        max_length=255,
        help_text=_("A short description not longer than 155 characters. Don't use double quotes."),
        blank=True,
    )

    keywords = models.CharField(
        verbose_name=_('keywords'),
        max_length=255,
        help_text=_("A comma-separated list of keywords. Don't use double quotes."),
        blank=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('owner'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_owned",
    )

    class Meta:
        abstract = True


class AbstractCategory(TimeStampedModel, MPTTModel):
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

    class Meta:
        abstract = True

    class MPTTMeta:
        order_insertion_by = ['created']


class AbstractAttachment(models.Model):
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('file name'),
    )

    # PK is a private identifier
    uid = models.UUIDField(
        verbose_name=_('public identifier'),
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )

    file = models.FileField(
        verbose_name=_('uploaded file'),
        upload_to="attachments",
    )

    created = models.DateTimeField(
        verbose_name=_('created time'),
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')

    def __str__(self):
        return self.name


class Google(TimeStampedModel):
    site_id = models.IntegerField(
        verbose_name=_('site id'),
    )

    analytics_uid = models.CharField(
        verbose_name=_('Google Analytics UA-ID'),
        max_length=128,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Google Service')
        verbose_name_plural = _('Google Services')
