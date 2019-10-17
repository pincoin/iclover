from django.contrib import admin
from design import models
from mptt.admin import DraggableMPTTAdmin

class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title')
    list_filter = ('parent','created')
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']

class SectorsCategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title')
    list_filter = ('parent','created')
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']

class ProductTextAdmin(admin.ModelAdmin):
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

class ProductImgAdmin(admin.ModelAdmin):
    pass

class CartProductAdmin(admin.ModelAdmin):
    pass

class CartPriceProblemAdmin(admin.ModelAdmin):
    pass

class ProductPriceAPIAdmin(admin.ModelAdmin):
    pass

class CustomerOrderInfoAdmin(admin.ModelAdmin):
    pass

class CustomerOrderProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.SectorsCategory, SectorsCategoryAdmin)
admin.site.register(models.ProductText, ProductTextAdmin)
admin.site.register(models.ProductPriceAPI, ProductPriceAPIAdmin)

admin.site.register(models.CustomerOrderInfo, CustomerOrderInfoAdmin)
admin.site.register(models.CustomerOrderProduct, CustomerOrderProductAdmin)

admin.site.register(models.OrderInfo, OrderInfoAdmin)
admin.site.register(models.OrderList, OrderListAdmin)
admin.site.register(models.OrderImg, OrderImgAdmin)
admin.site.register(models.OrderMemo, OrderMemoAdmin)

admin.site.register(models.ProductImg, ProductImgAdmin)
admin.site.register(models.CartProduct, CartProductAdmin)
admin.site.register(models.CartPriceProblem, CartPriceProblemAdmin)

