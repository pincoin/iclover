from django.contrib import admin
from .models import (
    Category, Option, SectorsCategory,
    StandardOption, PaperOption, DosuOption, ProductPrice,
    BusuOption,OrderImg,OrderInfo,OrderList,OrderMemo,

)
from mptt.admin import DraggableMPTTAdmin

class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug','is_removed')
    list_filter = ('parent','created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']

class SectorsCategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug')
    list_filter = ('parent','created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']


class StandardOptionAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'category', 'indented_title', 'slug')
    list_filter = ('category__title', 'created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']


class PaperOptionAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'category', 'indented_title', 'slug')
    list_filter = ('category__title', 'created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']

class DosuOptionAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'category', 'indented_title', 'slug')
    list_filter = ('category__title', 'created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']

class BusuOptionAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'category', 'indented_title', 'slug')
    list_filter = ('category__title', 'created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']

class OptionAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'category', 'indented_title', 'slug')
    list_filter = ('category__title', 'created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']

class ProductPriceAdmin(admin.ModelAdmin):
    list_filter = ('purchase', 'created')

class OrderInfoAdmin(admin.ModelAdmin):
    pass

class OrderListAdmin(admin.ModelAdmin):
    pass

class OrderImgAdmin(admin.ModelAdmin):
    pass

class OrderMemoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(SectorsCategory, SectorsCategoryAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(StandardOption, StandardOptionAdmin)
admin.site.register(PaperOption, PaperOptionAdmin)
admin.site.register(DosuOption, DosuOptionAdmin)
admin.site.register(BusuOption, BusuOptionAdmin)
admin.site.register(ProductPrice, ProductPriceAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(OrderList, OrderListAdmin)
admin.site.register(OrderImg, OrderImgAdmin)
admin.site.register(OrderMemo, OrderMemoAdmin)
