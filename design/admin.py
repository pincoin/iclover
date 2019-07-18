from django.contrib import admin
from design import models
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

class ProductBaseAdmin(admin.ModelAdmin):
    pass

class ProductTextAdmin(admin.ModelAdmin):
    pass

class PaperOptionAdmin(admin.ModelAdmin):
    pass

class StandardOptionAdmin(admin.ModelAdmin):
    pass

class SideOptionAdmin(admin.ModelAdmin):
    pass

class HooOptionAdmin(admin.ModelAdmin):
    pass

class DeliveryOptionAdmin(admin.ModelAdmin):
    pass

class EtcOptionAdmin(admin.ModelAdmin):
    pass

class OrderInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ['company','company_keyword']

class OrderListAdmin(admin.ModelAdmin):
    list_per_page = 10

class OrderImgAdmin(admin.ModelAdmin):
    list_per_page = 10

class OrderMemoAdmin(admin.ModelAdmin):
    list_per_page = 10

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.SectorsCategory, SectorsCategoryAdmin)
admin.site.register(models.ProductBase, ProductBaseAdmin)
admin.site.register(models.ProductText, ProductTextAdmin)
admin.site.register(models.PaperOption, PaperOptionAdmin)
admin.site.register(models.StandardOption, StandardOptionAdmin)
admin.site.register(models.SideOption, SideOptionAdmin)
admin.site.register(models.HooOption, HooOptionAdmin)
admin.site.register(models.DeliveryOption, DeliveryOptionAdmin)
admin.site.register(models.EtcOption, EtcOptionAdmin)
admin.site.register(models.OrderInfo, OrderInfoAdmin)
admin.site.register(models.OrderList, OrderListAdmin)
admin.site.register(models.OrderImg, OrderImgAdmin)
admin.site.register(models.OrderMemo, OrderMemoAdmin)
