from django.contrib import admin

from .models import (
    Product, Deposit, Discount, Employees, Ask, Sample
)


class ProductAdmin(admin.ModelAdmin):
    pass

class DepositAdmin(admin.ModelAdmin):
    pass

class DiscountAdmin(admin.ModelAdmin):
    pass

class EmployeesAdmin(admin.ModelAdmin):
    pass

class AskAdmin(admin.ModelAdmin):
    pass

class SampleAdmin(admin.ModelAdmin):
    pass




admin.site.register(Product, ProductAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Ask, AskAdmin)
admin.site.register(Sample, SampleAdmin)
