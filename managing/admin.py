from django.contrib import admin
from django.utils.safestring import mark_safe
from . import models as managing_models

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
    def get_queryset(self, request):
        qs = super(SampleAdmin, self).get_queryset(request)
        qs = qs.select_related('category','sectors_category','employees','category__parent','sectors_category__parent',).\
            prefetch_related('category__parent', 'sectors_category__parent')
        return qs

    list_per_page = 10
    list_display = ['image_tag', 'name', 'aspect','category',  'sectors_category', 'keyword', 'link', ]
    list_editable = ['aspect','category',  'sectors_category', 'keyword', 'link', ]
    readonly_fields = ['image_tag',]
    search_fields = ['name', 'keyword']

    # def images(self, obj):
    #     return mark_safe('<image src="/banner/media/%s" /width="100px">' % obj.file_name)

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
