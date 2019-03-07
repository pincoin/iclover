from django.contrib import admin
from .models import (
    Goods_banner,
)
class Goods_bannerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Goods_banner, Goods_bannerAdmin)
