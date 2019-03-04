from django.contrib import admin

from .models import (
    Product, Sample
)


class ProductAdmin(admin.ModelAdmin):
    pass

class SampleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Sample, SampleAdmin)
