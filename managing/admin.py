from django.contrib import admin

from .models import (
    Product, Deposit, Discount
)


class ProductAdmin(admin.ModelAdmin):
    pass

class DepositAdmin(admin.ModelAdmin):
    pass

class DiscountAdmin(admin.ModelAdmin):
    pass




admin.site.register(Product, ProductAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Discount, DiscountAdmin)

