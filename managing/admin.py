from django.contrib import admin

from . import models

class SpecialPriceAdmin(admin.ModelAdmin):
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

class MemoAdmin(admin.ModelAdmin):
    pass

class OrderWithDepositAdmin(admin.ModelAdmin):
    pass

class CustomerMemoAdmin(admin.ModelAdmin):
    pass




admin.site.register(models.SpecialPrice, SpecialPriceAdmin)
admin.site.register(models.Deposit, DepositAdmin)
admin.site.register(models.OrderWithDeposit, OrderWithDepositAdmin)
admin.site.register(models.Discount, DiscountAdmin)
admin.site.register(models.Employees, EmployeesAdmin)
admin.site.register(models.Ask, AskAdmin)
admin.site.register(models.Sample, SampleAdmin)
admin.site.register(models.Memo,MemoAdmin)
admin.site.register(models.CustomerMemo,CustomerMemoAdmin)
