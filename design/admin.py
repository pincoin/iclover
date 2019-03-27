from django.contrib import admin
from .models import (
    Goods_banner, Category, Option, OptionValue, SectorsCategory,
    StandardOption, StandardOptionValue, PaperOption, PaperOptionValue, DosuOption, DosuOptionValue,
    BusuOption, BusuOptionValue,

)
from mptt.admin import DraggableMPTTAdmin


class Goods_bannerAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug')
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

class StandardOptionValueAdmin(admin.ModelAdmin):
    pass

class PaperOptionAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'category', 'indented_title', 'slug')
    list_filter = ('category__title', 'created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']

class PaperOptionValueAdmin(admin.ModelAdmin):
    pass

class DosuOptionAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'category', 'indented_title', 'slug')
    list_filter = ('category__title', 'created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']

class DosuOptionValueAdmin(admin.ModelAdmin):
    pass

class BusuOptionAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'category', 'indented_title', 'slug')
    list_filter = ('category__title', 'created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']

class BusuOptionValueAdmin(admin.ModelAdmin):
    pass



class OptionAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'category', 'indented_title', 'slug')
    list_filter = ('category__title', 'created')
    prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20
    ordering = ['tree_id', 'lft']


class OptionValueAdmin(admin.ModelAdmin):
    pass



admin.site.register(Goods_banner, Goods_bannerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SectorsCategory, SectorsCategoryAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(OptionValue, OptionValueAdmin)
admin.site.register(StandardOption, StandardOptionAdmin)
admin.site.register(StandardOptionValue, StandardOptionValueAdmin)
admin.site.register(PaperOption, PaperOptionAdmin)
admin.site.register(PaperOptionValue, PaperOptionValueAdmin)
admin.site.register(DosuOption, DosuOptionAdmin)
admin.site.register(DosuOptionValue, DosuOptionValueAdmin)
admin.site.register(BusuOption, BusuOptionAdmin)
admin.site.register(BusuOptionValue, BusuOptionValueAdmin)